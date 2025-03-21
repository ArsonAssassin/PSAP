using Archipelago.Core;
using Archipelago.Core.MauiGUI;
using Archipelago.Core.MauiGUI.Models;
using Archipelago.Core.MauiGUI.ViewModels;
using Archipelago.Core.Models;
using Archipelago.Core.Util;
using Archipelago.MultiClient.Net.MessageLog.Messages;
using Microsoft.UI.Xaml;
using Newtonsoft.Json;
using Serilog;

namespace PSAP
{
    public partial class App : Microsoft.Maui.Controls.Application
    {
        static MainPageViewModel Context;
        public static ArchipelagoClient Client { get; set; }
        public static List<PokemonSnapItem> AllItems { get; set; }
        private static readonly object _lockObject = new object();
        public App()
        {
            InitializeComponent();
            var options = new GuiDesignOptions
            {
                BackgroundColor = Color.FromArgb("FFFCF5E5"),
                ButtonColor = Color.FromArgb("FFB3A125"),
                ButtonTextColor = Color.FromArgb("FF000000"),
                Title = "PSAP - Pokemon Snap Archipelago",
                TextColor = Color.FromArgb("FF000000")

            };

            Context = new MainPageViewModel(options);
            Context.ConnectClicked += Context_ConnectClicked;
            Context.CommandReceived += (e, a) =>
            {
                Client?.SendMessage(a.Command);
            };
            MainPage = new MainPage(Context);
            Context.ConnectButtonEnabled = true;
        }
        private async void Context_ConnectClicked(object? sender, ConnectClickedEventArgs e)
        {
            Context.ConnectButtonEnabled = false;
            Log.Logger.Information("Connecting...");
            if (Client != null)
            {
                Client.Connected -= OnConnected;
                Client.Disconnected -= OnDisconnected;
                Client.ItemReceived -= Client_ItemReceived;
                Client.MessageReceived -= Client_MessageReceived;
                Client.CancelMonitors();
            }
            GenericGameClient client = new GenericGameClient("Project64");
            var connected = client.Connect();
            if (!connected)
            {
                Log.Logger.Error("Project64 not running, open Project64 and load Pokemon Snap before connecting!");
                Context.ConnectButtonEnabled = true;
                return;
            }

            Client = new ArchipelagoClient(client);

            AllItems = Helpers.GetAllItems();
            Client.Connected += OnConnected;
            Client.Disconnected += OnDisconnected;
            await Client.Connect(e.Host, "Pokemon Snap");

            Client.ItemReceived += Client_ItemReceived;
            Client.MessageReceived += Client_MessageReceived;

            await Client.Login(e.Slot, !string.IsNullOrWhiteSpace(e.Password) ? e.Password : null);

            var photoLocations = Helpers.GetPhotographScoreLocations();
            Client.MonitorLocations(photoLocations);
            //SetCameraRoll(5);
            SetupToolAddresses();
            Context.ConnectButtonEnabled = true;
        }

        private static void LogItem(Item item)
        {
            var messageToLog = new LogListItem(new List<TextSpan>()
            {
                new TextSpan(){Text = $"[{item.Id.ToString()}] -", TextColor = Color.FromRgb(255, 255, 255)},
                new TextSpan(){Text = $"{item.Name}", TextColor = Color.FromRgb(200, 255, 200)},
                new TextSpan(){Text = $"x{item.Quantity.ToString()}", TextColor = Color.FromRgb(200, 255, 200)}
            });
            lock (_lockObject)
            {
                Microsoft.Maui.Controls.Application.Current.Dispatcher.DispatchAsync(() =>
                {
                    Context.ItemList.Add(messageToLog);
                });
            }
        }
        private void Client_MessageReceived(object? sender, Archipelago.Core.Models.MessageReceivedEventArgs e)
        {
            if (e.Message.Parts.Any(x => x.Text == "[Hint]: "))
            {
                LogHint(e.Message);
            }
            Log.Logger.Information(JsonConvert.SerializeObject(e.Message));
        }
        private static void Client_ItemReceived(object? sender, ItemReceivedEventArgs e)
        {
            LogItem(e.Item);
            var itemId = e.Item.Id;
            var itemToReceive = AllItems.FirstOrDefault(x => x.Id == itemId);

            if (itemToReceive.Type == Enums.ItemType.Tool)
            {
                EnableTool(itemToReceive);
            }
            else if (itemToReceive.Type == Enums.ItemType.Area)
            {
                SetUnlockedRoutes();
            }
        }
        private static void SetUnlockedRoutes()
        {
            var routeNames = new List<Tuple<string, byte, uint>>() { new Tuple<string, byte, uint>("Beach", 0x06, 0x80195918), new Tuple<string, byte, uint>("Tunnel", 0x07, 0x80195964), new Tuple<string, byte, uint>("Volcano", 0x08, 0x80195A60), new Tuple<string, byte, uint>("River", 0x09, 0x80195A1C), new Tuple<string, byte, uint>("Cave", 0x0A, 0x801959BC), new Tuple<string, byte, uint>("Valley", 0x0B, 0x80195AA8), new Tuple<string, byte, uint>("Rainbow Cloud", 0x0C, 0x80195AFC) };
            var routes = Client.GameState.ReceivedItems.Where(x => routeNames.Any(y => y.Item1.Contains(x.Name)));
            var offset = 0;
            foreach (var route in routeNames)
            {
                if (routes.Any(x => x.Name.Contains(route.Item1)))
                {
                    //Set menu item
                    Memory.WriteByte((ulong)(Addresses.Project64Offset + Addresses.RouteTable + offset), route.Item2);
                    offset++;
                    //set menu text
                    Memory.Write((ulong)(Addresses.Project64Offset + Addresses.RouteTable + offset), route.Item3);
                    offset +=7;
                }
            }
            //Add return button
            Memory.WriteByte((ulong)(Addresses.Project64Offset + Addresses.RouteTable + offset), 0x05);
            offset++;
            Memory.Write((ulong)(Addresses.Project64Offset + Addresses.RouteTable + offset), 0x80195B48);            
            offset += 7;
            //Terminate Menu
            Memory.WriteByte((ulong)(Addresses.Project64Offset + Addresses.RouteTable + offset), 0x23);
            offset++;
            Memory.Write((ulong)(Addresses.Project64Offset + Addresses.RouteTable + offset), 0x00000000);
            offset += 7;
        }
        private static void SetupToolAddresses()
        {
            Memory.Write(Addresses.Project64Offset + 0x00350A54, Addresses.Project64Offset + 0x00980000);
            Memory.Write(Addresses.Project64Offset + 0x003509F0, Addresses.Project64Offset + 0x008C0001);
            Memory.Write(Addresses.Project64Offset + 0x00350984, Addresses.Project64Offset + 0x00980002);
            Memory.Write(Addresses.Project64Offset + 0x003AE51F, 0x04);
            Memory.WriteBit(Addresses.Project64Offset + 0x000C2226, 3, true);
        }
        private void SetCameraRoll(ushort size)
        {

            Memory.Write(Addresses.Project64Offset + 0x0009CEA8, 0x3C1C800C);
            Memory.Write(Addresses.Project64Offset + 0x0035E51C, 0x8F8E21FF);
            Memory.Write(Addresses.Project64Offset + 0x0035E53C, 0x8F8E21FF);
            Memory.Write(Addresses.Project64Offset + 0x00353828, 0x8F8421FF);
            Memory.Write(Addresses.Project64Offset + 0x0009CA18, 0x00E4082A);

            Memory.Write(Addresses.Project64Offset + Addresses.CameraRollSize, size);
        }
        private static void EnableTool(PokemonSnapItem tool)
        {
            switch (tool.Name)
            {
                case ("Apple Unlocked"):
                    Memory.Write(Addresses.Project64Offset + Addresses.Apple, 0x01);
                    break;
                case ("Pester Ball Unlocked"):
                    Memory.Write(Addresses.Project64Offset + Addresses.PesterBall, 0x02);
                    break;
                case ("Flute Unlocked"):
                    Memory.Write(Addresses.Project64Offset + Addresses.Flute, 0x03);
                    break;
                case ("Speed Boost Unlocked"):
                    Memory.Write(Addresses.Project64Offset + Addresses.SpeedBoost, 0x24);
                    break;
                default:
                    throw new ArgumentOutOfRangeException(nameof(tool));
            }
        }
        private static void LogHint(LogMessage message)
        {
            var newMessage = message.Parts.Select(x => x.Text);

            if (Context.HintList.Any(x => x.TextSpans.Select(y => y.Text) == newMessage))
            {
                return; //Hint already in list
            }
            List<TextSpan> spans = new List<TextSpan>();
            foreach (var part in message.Parts)
            {
                spans.Add(new TextSpan() { Text = part.Text, TextColor = Color.FromRgb(part.Color.R, part.Color.G, part.Color.B) });
            }
            lock (_lockObject)
            {
                Microsoft.Maui.Controls.Application.Current.Dispatcher.DispatchAsync(() =>
                {
                    Context.HintList.Add(new LogListItem(spans));
                });
            }
        }
        private static void OnConnected(object sender, EventArgs args)
        {
            Log.Logger.Information("Connected to Archipelago");
            Log.Logger.Information($"Playing {Client.CurrentSession.ConnectionInfo.Game} as {Client.CurrentSession.Players.GetPlayerName(Client.CurrentSession.ConnectionInfo.Slot)}");
        }

        private static void OnDisconnected(object sender, EventArgs args)
        {
            Log.Logger.Information("Disconnected from Archipelago");
        }
        protected override Microsoft.Maui.Controls.Window CreateWindow(IActivationState activationState)
        {
            var window = base.CreateWindow(activationState);
            if (DeviceInfo.Current.Platform == DevicePlatform.WinUI)
            {
                window.Title = "PSAP - Pokemon Snap Archipelago Randomizer";

            }
            window.Width = 600;

            return window;
        }
    }
}
