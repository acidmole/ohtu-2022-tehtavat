import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):

    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.varasto_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock.saldo.side_effect = self.varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = self.varasto_hae_tuote

        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    def varasto_saldo(self, tuote_id):
        if tuote_id == 1:
            return 10
        elif tuote_id == 2:
            return 10
        elif tuote_id == 3:
            return 0

    def varasto_hae_tuote(self, tuote_id):
        if tuote_id == 1:
            return Tuote(1, "maito", 5)
        elif tuote_id == 2:
            return Tuote(2, "leipä", 10)
        elif tuote_id == 3:
            return Tuote(3, "juusto", 17)



    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called()

    def test_tilimaksu_toimii_oikein(self):
        
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 5)

    def test_kahden_eri_tuotteen_osto_toimii_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", ANY, "12345", ANY, 15)

    def test_kahden_saman_tuotteen_osto_toimii_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("janne", "54321")

        self.pankki_mock.tilisiirto.assert_called_with("janne", ANY, "54321", ANY, 20)

    def test_toinen_tuote_on_loppu_toimii_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("janne", "54321")

        self.pankki_mock.tilisiirto.assert_called_with("janne", ANY, "54321", ANY, 10)

    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)

        self.kauppa.tilimaksu("janne", "54321")

        self.pankki_mock.tilisiirto.assert_called_with("janne", ANY, "54321", ANY, 10)

    def test_kauppa_pyytää_uuden_viitenumeron_jokaiselle_maksutapahtumalle(self):

        self.viitegeneraattori_mock.uusi.side_effect = [1, 2, 3]
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)

        self.kauppa.tilimaksu("janne", "54321")
        self.pankki_mock.tilisiirto.assert_called_with("janne", 1, "54321", ANY, 10)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)

        self.kauppa.tilimaksu("janne", "54321")
        self.pankki_mock.tilisiirto.assert_called_with("janne", 2, "54321", ANY, 10)

    def test_poista_tuote_toimii_oikein(self):

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.poista_korista(2)

        self.varasto_mock.palauta_varastoon.assert_called()