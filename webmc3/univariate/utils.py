from math import ceil, floor


def get_ix_slice(relayoutData):
    if relayoutData is None:
        return None
    else:
        try:
            return slice(
                floor(relayoutData['xaxis.range[0]']),
                ceil(relayoutData['xaxis.range[1]'])
            )
        except KeyError:
            return None
