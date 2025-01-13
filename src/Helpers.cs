using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using Location = Archipelago.Core.Models.Location;
namespace PSAP
{
    public static class Helpers
    {
        public static List<PokemonSnapItem> GetItems()
        {
            var json = OpenEmbeddedResource("PSAP.Resources.Items.json");
            var list = JsonConvert.DeserializeObject<List<PokemonSnapItem>>(json);
            return list;
        }
        public static List<PokemonSnapItem> GetAllItems()
        {
            var results = new List<PokemonSnapItem>();

            results = results.Concat(GetItems()).ToList();

            return results;
        }
        public static List<Location> GetPhotographScoreLocations()
        {
            var json = OpenEmbeddedResource("PSAP.Resources.Locations.json");
            var list = JsonConvert.DeserializeObject<List<Location>>(json);
            return list;
        }
        public static string OpenEmbeddedResource(string resourceName)
        {
            var assembly = Assembly.GetExecutingAssembly();
            using (Stream stream = assembly.GetManifestResourceStream(resourceName))
            using (StreamReader reader = new StreamReader(stream))
            {
                string file = reader.ReadToEnd();
                return file;
            }
        }
    }
}
