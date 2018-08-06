import numpy as np
from skimage.measure import label, regionprops
from skimage.filters import gaussian
from skimage.util.dtype import convert
import mahotas as mh


options = {
    'min_size': 0,
    'threshold': None,
    'bkg': None,
}


def find_centroids(img, bkg=None, threshold=None, min_size=0):
    if bkg is None:
        bkg = gaussian(img, 10)
    bkg.astype(np.uint16)
    img = convert(img-bkg,np.uint8) #<- This changes the execution speed ~5-fold
    if threshold is None:
        threshold = mh.otsu(img)
#     mask = img>threshold
#     labels = np.array(mh.label(img>threshold)[0])
    labels = label(img>threshold)  # <- This is faster
    props = regionprops(labels, img, cache=True)  # <- Cache True is faster
#     num_pixels = [p['filled_area'] for p in props]
    centroids = [p['centroid'] for p in props if p['filled_area']>=min_size]
    return centroids