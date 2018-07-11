import trackpy as tp


options = {
    'diameter': 1,    # Min Diameter of the features
    'minmass': 1,     # Min brightness of the features
    'maxsize': None,     # Maximum radius-of-gyration
    'separation': None,  # Minimum separation between features
}


def find_centroids(**kwargs):
    """Locates the centroids of the features based on the specify library. In this case we are using Trackpy.
    .. warning:: We should deprecate the use of trackpy and made a custom-solution
    """