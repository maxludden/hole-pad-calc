import pytest
from hole_pad_calc.rect_calc import RectCalc, Measurement
import pytest
from hole_pad_calc.rect_calc import RectCalc, Measurement

@pytest.fixture
def rect_calc():
    # Setup code to create an instance of RectCalc
    return RectCalc(Measurement(1.0, 'mm'), Measurement(1.0, 'mm'))

def test_table_generation(rect_calc):
    # Test the table generation method
    table = rect_calc.generate_table(places=2)

    # Check the table content for mm conversion
    assert table.rows[0] == [
        100,  # length in mm
        50,   # width in mm
        111.8,  # hypo in mm
        20,   # hole_size in mm
        10    # pad_size in mm
    ]

    # Check the table content for mil conversion
    assert table.rows[1] == [
        pytest.approx(3937.01, 0.01),  # length in mil
        pytest.approx(1968.5, 0.01),   # width in mil
        pytest.approx(4403.15, 0.01),  # hypo in mil
        pytest.approx(787.4, 0.01),    # hole_size in mil
        pytest.approx(393.7, 0.01)     # pad_size in mil
    ]

def test_text_assembly(rect_calc):
    # Test the text assembly part
    text_assembled = rect_calc.assemble_text(places=2)

    # Check the text content
    assert str(text_assembled[0]) == "100.00 mm"
    assert str(text_assembled[1]) == "50.00 mm"
    assert str(text_assembled[2]) == "111.80 mm"
    assert str(text_assembled[3]) == "20.00 mm"
    assert str(text_assembled[4]) == "10.00 mm"
    @pytest.fixture
    def rect_calc():
        # Setup code to create an instance of RectCalc
        return RectCalc(Measurement(1.0, 'mm'), Measurement(1.0, 'mm'))

    def test_calc_hypo(rect_calc):
        # Test the calc_hypo method
        hypo = rect_calc.calc_hypo(Measurement(3.0, 'in'), Measurement(4.0, 'in'))
        assert hypo.value == pytest.approx(5.0, 0.01)
        assert hypo.unit == 'in'

    def test_calc_hole(rect_calc):
        # Test the calc_hole method
        hole_size = rect_calc.calc_hole(Measurement(3.0, 'in'), Measurement(4.0, 'in'))
        assert hole_size.value == pytest.approx(5.01, 0.01)
        assert hole_size.unit == 'in'

    def test_calc_pad(rect_calc):
        # Test the calc_pad method
        pad_size = rect_calc.calc_pad(Measurement(3.0, 'in'), Measurement(4.0, 'in'))
        assert pad_size.value == pytest.approx(5.027, 0.01)
        assert pad_size.unit == 'in'

    def test_table_generation(rect_calc):
        # Test the table generation method
        table = rect_calc.generate_table(places=2)

        # Check the table content for mm conversion
        assert table.rows[0] == [
            100,  # length in mm
            50,   # width in mm
            111.8,  # hypo in mm
            20,   # hole_size in mm
            10    # pad_size in mm
        ]

        # Check the table content for mil conversion
        assert table.rows[1] == [
            pytest.approx(3937.01, 0.01),  # length in mil
            pytest.approx(1968.5, 0.01),   # width in mil
            pytest.approx(4403.15, 0.01),  # hypo in mil
            pytest.approx(787.4, 0.01),    # hole_size in mil
            pytest.approx(393.7, 0.01)     # pad_size in mil
        ]

    def test_text_assembly(rect_calc):
        # Test the text assembly part
        text_assembled = rect_calc.assemble_text(places=2)

        # Check the text content
        assert str(text_assembled[0]) == "100.00 mm"
        assert str(text_assembled[1]) == "50.00 mm"
        assert str(text_assembled[2]) == "111.80 mm"
        assert str(text_assembled[3]) == "20.00 mm"
        assert str(text_assembled[4]) == "10.00 mm"
if __name__ == '__main__':
    pytest.main()
