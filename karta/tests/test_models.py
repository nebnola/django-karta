from django.test import TestCase

from ..models import Ansicht, Karte, Ablageort


class AnsichtModelTests(TestCase):
    def test_masstab_formatting(self):
        ansicht = Ansicht(massstab=20000)
        self.assertEqual(ansicht.massstab_f, "1:20000")

    def test_massstab_unknown(self):
        ansicht = Ansicht()
        self.assertEqual(ansicht.massstab_f, "Unbekannt")


class KarteModelTests(TestCase):
    def setUp(self):
        ablage=Ablageort(name="blabla")
        ablage.save()
        self.karte = Karte(ablageort=ablage)
        self.karte.save()

    def test_geojson_set_no_ansichten(self):
        #TODO: disallow Karte without any Ansicht in future?
        self.assertListEqual(self.karte.geojson_set(),[])

    def test_geojson_set_no_coordinates(self):
        ansicht = Ansicht(karte=self.karte, massstab=50_000)
        ansicht.save()
        self.assertListEqual(self.karte.geojson_set(),[])

class KarteModelTestGeojson(TestCase):
    @classmethod
    def setUpTestData(cls):
        ablage=Ablageort(name="blabla")
        ablage.save()
        cls.karte = Karte(ablageort=ablage)
        cls.karte.save()
        #TODO: consider floating point precision?
        a1 = Ansicht(karte=cls.karte, massstab=200_000)
        a2 = Ansicht(karte=cls.karte, massstab=20_000,koords=[
            [0.123,12.456],
            [0.123,15.111],
            [1.1115,15.111],
            [1.1118,12.456],
            [0.123,12.456]
        ], kurzbeschreibung="Tolle Karte")
        a3 = Ansicht(karte=cls.karte, koords = [
            [-68.554688, 36.879621],
            [-59.765625, 36.315125],
            [-56.601563, 40.580585],
            [-68.554688, 36.879621]
          ]
        )
        for a in (a1,a2,a3):
            a.save()

    def test_number_of_features(self):
        self.assertEqual(len(self.karte.geojson_set()),2)

    def test_signature1(self):
        self.assertEqual(list(self.karte.geojson_set()[0].keys()),["type","properties","geometry"])

    def test_properties1(self):
        feat1 = self.karte.geojson_set()[0]
        self.assertEqual(feat1["properties"]["description"], "Tolle Karte")
        self.assertEqual(feat1["properties"]["massstab"], "1:20000")

    def test_properties2(self):
        feat2 = self.karte.geojson_set()[1]
        self.assertIs(feat2["properties"]["description"], "")
        self.assertIs(feat2["properties"]["massstab"], "Unbekannt")

    def test_geometry1(self):
        self.assertEqual(self.karte.geojson_set()[0]["geometry"],
                         {
                             "type": "Polygon",
                             "coordinates":  [[[0.123,12.456],
                                            [0.123,15.111],
                                            [1.1115,15.111],
                                            [1.1118,12.456],
                                            [0.123,12.456]]]
                         })
