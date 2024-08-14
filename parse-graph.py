import io
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


with open('graph', "rb") as fh:
    buf = BytesIO(fh.read())

print(buf)

buf.seek(0)
plt.imread(buf)

buf.close()