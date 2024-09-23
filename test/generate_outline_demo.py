from pathlib import Path
import sys
PROJECT_PATH = Path(__file__).parent.parent.resolve()
sys.path.append(str(PROJECT_PATH))
from src import generate_outline_gr

if __name__ == "__main__":
    print(generate_outline_gr("太阳系简介",3,4))