import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42
        self.varasto_mock = Mock()
        self.saldot = {1: 10, 2: 10}

        def varasto_saldo(tuote_id):
            return self.saldot.get(tuote_id)

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipa", 3)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote
        self.kauppa = Kauppa(
            self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock
        )

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_maksettaessa_ostos_tilisiirtoa_kutsutaan_oikeilla_tiedoilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", ANY, "12345", "33333-44455", 5
        )

    def test_maksettaessa_kaksi_eri_tuotetta_tilisiirtoa_kutsutaan_oikeilla_tiedoilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", ANY, "12345", "33333-44455", 8
        )

    def test_maksettaessa_kaksi_samaa_tuotetta_tilisiirtoa_kutsutaan_oikeilla_tiedoilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", ANY, "12345", "33333-44455", 10
        )

    def test_maksettaessa_loppunutta_tuotetta_ei_lasketa_summaan(self):
        self.saldot[2] = 0

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", ANY, "12345", "33333-44455", 5
        )

    def test_asioinnin_aloittaminen_nollaa_edellisen_ostoksen_tiedot(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", ANY, "12345", "33333-44455", 5
        )

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", ANY, "12345", "33333-44455", 3
        )

    def test_jokaiselle_maksutapahtumalle_pyydetaan_uusi_viitenumero(self):
        self.viitegeneraattori_mock.uusi.side_effect = [42, 43]

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.viitegeneraattori_mock.uusi.assert_called_once_with()
        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)
        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 43, "12345", "33333-44455", 3
        )

    def test_korista_poistetaan_vain_yksi_kappale_ja_palautetaan_varastoon(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)

        self.kauppa.poista_korista(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.varasto_mock.palauta_varastoon.assert_called_once_with(
            Tuote(1, "maito", 5)
        )
        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", ANY, "12345", "33333-44455", 8
        )
