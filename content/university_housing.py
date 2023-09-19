from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd
import numpy as np


def find_housing_idxs(df: pd.DataFrame, housing_locations: dict):
    # make every street number a tuple for convenience
    building = dict(housing_locations)

    indices = defaultdict(lambda: np.zeros(len(df), dtype=bool))

    def _find_idx(street_num, street_name):
        idx = [
            street in street_name for street in df["Residential Address Street Name"]
        ]

        if street_num is not None:
            if not isinstance(street_num, Iterable):
                # turn single number addr into iterableto match places
                # with multiple addresses
                street_num = (street_num,)
                # multiple valid street numbers
            idx = np.logical_and(
                idx,
                [num in street_num for num in df["Residential Address Street Number"]],
            )

        return idx

    for name, v in building.items():
        if isinstance(v, list):
            # complex with multiple addresses - e.g. holden green
            for addr in v:
                indices[name] |= _find_idx(addr[0], addr[1])
        else:
            indices[name] |= _find_idx(v[0], v[1])

    for name, idx in indices.items():
        df.loc[idx, "univ_housing_name"] = name
    indices["all"] = np.any(list(indices.values()), axis=0)
    return indices


gsas_dorms = ["Richards hl", "Perkins hl", "Conant hl", "Child hl"]
gsas_dorms = {name: (None, name.upper()) for name in gsas_dorms}
harvard_ugrad_houses = [
    h + " House"
    for h in [
        "Leverett",
        "Pforzheimer",
        "Adams",
        "Currier",
        "Cabot",
        "Dunster",
        "Eliot",
        "Kirkland",
        "Lowell",
        "Mather",
        "Quincy",
        "Winthrop",
    ]
]
harvard_ugrad_houses = {name: (None, name.upper()) for name in harvard_ugrad_houses}

hvd_law_dorms = [
    "Dane hl",
    "Ames hl",
    "Shaw hl",
    "Story hl",
    "Holmes hl",
    "Hastings hl",
    "North hl",
]
hvd_law_dorms = {name: (None, name.upper()) for name in hvd_law_dorms}


harvard_housing = {
    "Peabody Terrace": (None, "PEABODY TER"),
    "Holden Green": [
        (None, "HOLDEN GRN"),
        (list(range(10, 38 + 2, 2)), "HOLDEN ST"),
    ],  # multiple address here. the func will handle this
    "29 Garden St": (29, "GARDEN ST"),
    "Botanic Gardens": (None, "FERNALD DR"),
    "Kirkland Court": ((37, 39, 31), "KIRKLAND ST"),
    "10 Akron": (10, "AKRON ST"),
    "Ware St": (
        (9, 11, 13, 15, 17, 19),
        "WARE ST",
    ),
    # as it stands the function won't differentiate
    # between 13 and 13A ware st so should pick up both
    "Prescott": (list(range(85, 95 + 1, 2)), "PRESCOTT ST"),
}

harvard_1st_year = [
    "Greenough HL",
    "Hurlbut HL",
    "Pennypacker HL",
    "Wigglesworth HL",
    "Grays HL",
    "Matthews HL",
    "Weld HL",
    "Apley CT",
    "Hollis HL",
    "Holworthy HL",
    "Lionel HL",
    "Mass HL",
    "Mower HL",
    "Stoughton HL",
    "Straus HL",
    "Canaday HL",
    "Thayer HL",
]

harvard_1st_year = {name: (None, name.upper()) for name in harvard_1st_year}

mit_dorms = {
    "Baker House": (362, "MEMORIAL DR"),
    "Burton Conner": (410, "MEMORIAL DR"),
    "East Campus": (3, "AMES ST"),
    "MacGregor House": (450, "MEMORIAL DR"),
    "Maseeh Hall": (305, "MEMORIAL DR"),
    "McCormick Hall": (320, "MEMORIAL DR"),
    "New House": (tuple(range(471, 476 + 1)), "MEMORIAL DR"),
    "Next House": (500, "MEMORIAL DR"),
    "New Vassar": (189, "VASSAR ST"),
    "Random Hall": (290, "MASSACHUSETTS AVE"),
    "Simmons Hall": (tuple(range(229, 243 + 1)), "VASSAR ST"),
}


mit_grad_housing = {
    "70 Amherst": (70, "AMHERST ST"),
    "Ashdown": (235, "ALBANY ST"),
    "Edgerton": (143, "ALBANY ST"),
    "Grad Tower": (45, "HAYWARD ST"),
    "Sidney Pacific": (70, "PACIFIC ST"),
    "Tang Hall": (550, "MEMORIAL DR"),
    "The Warehouse": (224, "ALBANY ST"),
    "Westgate": (540, "MEMORIAL DRIVE"),
}

lesley_housing = {
    "Doble": (30, "MELLEN ST"),
    "Compass House": (14, "WENDELL ST"),
    "Everett House": (28, "WENDELL ST"),
    "Jenckes House": (31, "MELLEN ST"),
    "Kidder House": ((2, 4), "SAINT JOHNS RD"),
    "[Lesley] Kirkland House": (61, "OXFORD ST"),
    "Kris House": (68, "OXFORD ST"),
    "Lawrence Hall": (99, "BRATTLE ST"),
    "MacKenzie Hall": (36, "MELLEN ST"),
    "Malloch Hall": (38, "MELLEN ST"),
    "Mellen House": (24, "MELLEN ST"),
    "Rousmaniere House": (6, "SAINT JOHNS RD"),
    "Wendell House": (63, "OXFORD ST"),
    "White Hall": (33, "EVERETT ST"),
    "Wilbur House": (78, "OXFORD ST"),
    "Wilson House": ((16, 18), "WENDELL ST"),
    "Winthrop Hall": (list(range(1, 7 + 1, 2)), "SAINT JOHNS RD"),
    "Wolfard Hall": (34, "MELLEN ST"),
}
