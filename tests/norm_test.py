"""A."""

import unittest

from big5.norm import Norm


class NormTest(unittest.TestCase):
    def test_invalid_params(self) -> None:
        with self.assertRaises(TypeError):
            norm = Norm()

        with self.assertRaises(TypeError):
            norm = Norm(sex='M')

        with self.assertRaises(TypeError):
            norm = Norm(age=0)

        with self.assertRaises(AssertionError):
            norm = Norm(sex='M', age=1)

        with self.assertRaises(AssertionError):
            norm = Norm(sex='-', age=1)

        with self.assertRaises(AssertionError):
            norm = Norm(sex='F', age=121)

        with self.assertRaises(AssertionError):
            norm = Norm(sex='5', age=5)

    def test_norm_output(self) -> None:
        def check(d: dict) -> bool:
            assert isinstance(d, dict), 'norm must be a dict'

            self.assertIn('id', d.keys())
            self.assertIn('ns', d.keys())
            self.assertIn('category', d.keys())
            self.assertEqual(len(d), 3)

            assert isinstance(d.get('ns'), list), 'norm must be a list'
            self.assertEqual(len(d.get('ns')), 71)
            return True

        norm = Norm(sex='M', age=18)
        assert check(d=norm), 'common failed check 1'
        self.assertEqual(norm.get('id'), 1)
        self.assertEqual(norm.get('category'), 'men under 21 years old')

        norm = Norm(sex='F', age=18)
        assert check(d=norm), 'common failed check 2'
        self.assertEqual(norm.get('id'), 5)
        self.assertEqual(norm.get('category'), 'women under 21 years old')

        norm = Norm(sex='M', age=21)
        assert check(d=norm), 'common failed check 3'
        self.assertEqual(norm.get('id'), 2)
        self.assertEqual(norm.get('category'), 'men between 21 and 40 years old')

        norm = Norm(sex='F', age=30)
        assert check(d=norm), 'common failed check 4'
        self.assertEqual(norm.get('id'), 6)
        self.assertEqual(norm.get('category'), 'women between 21 and 40 years old')

        norm = Norm(sex='M', age=41)
        assert check(d=norm), 'common failed check 5'
        self.assertEqual(norm.get('id'), 3)
        self.assertEqual(norm.get('category'), 'men between 41 and 60 years of age')

        norm = Norm(sex='F', age=41)
        assert check(d=norm), 'common failed check 6'
        self.assertEqual(norm.get('id'), 7)
        self.assertEqual(norm.get('category'), 'women between 41 and 61 years old')

        norm = Norm(sex='M', age=60)
        assert check(d=norm), 'common failed check 7'
        self.assertEqual(norm.get('id'), 3)
        self.assertEqual(norm.get('category'), 'men between 41 and 60 years of age')

        norm = Norm(sex='F', age=60)
        assert check(d=norm), 'common failed check 8'
        self.assertEqual(norm.get('id'), 7)
        self.assertEqual(norm.get('category'), 'women between 41 and 61 years old')

        norm = Norm(sex='M', age=61)
        assert check(d=norm), 'common failed check 9'
        self.assertEqual(norm.get('id'), 4)
        self.assertEqual(norm.get('category'), 'men over 60 years old')

        norm = Norm(sex='F', age=61)
        assert check(d=norm), 'common failed check 10'
        self.assertEqual(norm.get('id'), 8)
        self.assertEqual(norm.get('category'), 'women over 60 years old')

        norm = Norm(sex='M', age=80)
        assert check(d=norm), 'common failed check 11'
        self.assertEqual(norm.get('id'), 4)
        self.assertEqual(norm.get('category'), 'men over 60 years old')

        norm = Norm(sex='F', age=80)
        assert check(d=norm), 'common failed check 10'
        self.assertEqual(norm.get('id'), 8)
        self.assertEqual(norm.get('category'), 'women over 60 years old')

        norm = Norm(sex='M', age=101)
        assert check(d=norm), 'common failed check 11'
        self.assertEqual(norm.get('id'), 4)
        self.assertEqual(norm.get('category'), 'men over 60 years old')

        norm = Norm(sex='F', age=105)
        assert check(d=norm), 'common failed check 12'
        self.assertEqual(norm.get('id'), 8)
        self.assertEqual(norm.get('category'), 'women over 60 years old')

    def test_static_calc(self):
        normc = Norm.calc(
            domain={'O': 0, 'C': 0, 'E': 0, 'A': 0, 'N': 0},
            norm=Norm(sex='M', age=40),
        )

        self.assertEqual(round(normc.get('O'), 2), -18.39)
        self.assertEqual(round(normc.get('C'), 2), -9.92)
        self.assertEqual(round(normc.get('E'), 2), -1.87)
        self.assertEqual(round(normc.get('A'), 2), -14.29)
        self.assertEqual(round(normc.get('N'), 2), 9.36)

        normc = Norm.calc(
            domain={'O': 99, 'C': 99, 'E': 99, 'A': 99, 'N': 99},
            norm=Norm(sex='M', age=40),
        )

        self.assertGreaterEqual(normc.get('O'), 59)
        self.assertGreaterEqual(normc.get('C'), 59)
        self.assertGreaterEqual(normc.get('E'), 63)
        self.assertGreaterEqual(normc.get('A'), 61)
        self.assertGreaterEqual(normc.get('N'), 69)

        normc = Norm.calc(
            domain={'O': 150, 'C': 150, 'E': 150, 'A': 150, 'N': 150},
            norm=Norm(sex='F', age=25),
        )

        self.assertGreaterEqual(normc.get('O'), 100)
        self.assertGreaterEqual(normc.get('C'), 95)
        self.assertGreaterEqual(normc.get('E'), 97)
        self.assertGreaterEqual(normc.get('A'), 101)
        self.assertGreaterEqual(normc.get('N'), 98)

        a = Norm.calc(
            domain={'N': 61, 'A': 87, 'C': 102, 'E': 66, 'O': 78},
            norm=Norm(sex='M', age=40),
        )

        b = Norm.calc(
            domain={'O': 78, 'C': 102, 'E': 66, 'A': 87, 'N': 61},
            norm=Norm(sex='M', age=40),
        )

        self.assertEqual(a, b)
        self.assertEqual(round(a.get('O'), 2), 43.27)
        self.assertEqual(round(b.get('C'), 2), 61.56)
        self.assertEqual(round(a.get('E'), 2), 41.52)
        self.assertEqual(round(b.get('A'), 2), 52.12)
        self.assertEqual(round(a.get('N'), 2), 46.38)


if __name__ == "__main__":
    order = ['test_invalid_params', 'test_norm_output', 'test_static_calc']
    loader = unittest.TestLoader()
    loader.sortTestMethodsUsing = lambda x, y: order.index(x) - order.index(y)
    unittest.main(testLoader=loader, verbosity=2)
