import pytest
import readchar

@pytest.fixture
def mock_readchar():
    """Fixture to mock readchar module."""
    with pytest.MonkeyPatch() as mp:
        mp.setattr(readchar, 'key', type('Key', (), {
            'UP': '\x1b[A',
            'ESC': '\x1b',
        }))
        yield readchar 