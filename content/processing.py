from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from numpy import dtype

_history_dtypes = {
    "Party Affiliation ": dtype("O"),
    "Voter ID Number ": dtype("O"),
    "Last Name ": dtype("O"),
    "First Name ": dtype("O"),
    "Middle Name ": dtype("O"),
    "Residential Address - Street Number": dtype("int64"),
    "Residential Address - Street Suffix ": dtype("O"),
    "Residential Address - Street Name ": dtype("O"),
    "Residential Address - Apartment Number ": dtype("O"),
    "Residential Address - Zip Code ": dtype("O"),
    "Type of Election ": dtype("O"),
    "Election Date ": dtype("O"),
    "City/ Town Name ": dtype("O"),
    "City/ Town Indicator ": dtype("O"),
    "City/ Town Code Assigned Number": dtype("int64"),
    "Voter Title ": dtype("O"),
    "Ward Number ": dtype("int64"),
    "Precinct Number ": dtype("O"),
    "Voter Status r": dtype("O"),
    "Mailing Address - Street Number/Name ": dtype("O"),
    "Mailing Address - Apartment Number ": dtype("O"),
    "Mailing Address - City/Town ": dtype("O"),
    "Mailing Address - State ": dtype("O"),
    "Mailing Address - Zip Code": dtype("O"),
    "Unnamed: 24": dtype("float64"),
}


_voter_list_dtypes = {
    "Record Sequence Number ": dtype("int64"),
    "Voter ID Number ": dtype("O"),
    "Last Name ": dtype("O"),
    "First Name ": dtype("O"),
    "Middle Name ": dtype("O"),
    "Title ": dtype("O"),
    "Residential Address Street Number ": dtype("int64"),
    "Residential Address Street Suffix ": dtype("O"),
    "Residential Address Street Name ": dtype("O"),
    "Residential Address Apartment Number ": dtype("O"),
    "Residential Address Zip Code ": dtype("O"),
    "Mailing Address ¿ Street Number and Name ": dtype("O"),
    "Mailing Address ? Street Number and Name ": dtype("O"),
    "Mailing Address - Apartment Number ": dtype("O"),
    "Mailing Address - City or Town ": dtype("O"),
    "Mailing Address - State": dtype("O"),
    "Mailing Address - Zip Code ": dtype("O"),
    "Party Affiliation ": dtype("O"),
    "Date of Birth ": dtype("O"),
    "Date of Registration ": dtype("O"),
    "Ward Number ": dtype("int64"),
    "Precinct Number ": dtype("O"),
    "Congressional District Number ": dtype("int64"),
    "Senatorial District Number ": dtype("int64"),
    "State Representative District ": dtype("int64"),
    "Voter Status": dtype("O"),
    "Unnamed: 25": dtype("float64"),
}


def load_try_encodings(file: str, dtypes):
    try:
        return pd.read_csv(file, delimiter="|", encoding="utf-8", dtype=dtypes)
    except UnicodeDecodeError:
        return pd.read_csv(file, delimiter="|", encoding="ISO-8859-1", dtype=dtypes)


def load_year(
    voter_history: str,
    voter_list: str,
):
    history = load_try_encodings(voter_history, dtypes=_history_dtypes)
    vlist = load_try_encodings(voter_list, _voter_list_dtypes)
    history.rename({c: c.strip() for c in history.columns}, inplace=True, axis=1)
    vlist.rename({c: c.strip() for c in vlist.columns}, inplace=True, axis=1)

    # manual corrections
    #
    history = history.set_index("Voter ID Number")
    vlist = vlist.set_index("Voter ID Number")
    drop_ids = [
        # erroneously entered reg with birth year of 1191
        # re-registered with different id the same year
        "02CLS2791002",
        # 2015 birthdays that are unclear how to correct
        "01GSR0112000",  #    01/01/1812
        "01MCN0112006",  #    01/01/1812
        "01ANE0112001",  #    01/01/1812
        "01WXO0109000",  #    01/01/1809
        # 2013 birthdays that unclear how to correct
        "01ACE0108001",  #    01/01/1808
        "01SEN0108008",  #    01/01/1808
        "01HPL0108001",  #    01/01/1808
        "01RKL0108001",  #    01/01/1808
        "01ARA0108004",  #    01/01/1808
        "01MRT0108003",  #    01/01/1808
        "01DOA0107001",  #    01/01/1807
        "01CBN0108003",  #    01/01/1808
        "01BRD0108006",  #    01/01/1808
        "01PAN0107002",  #    01/01/1807
        "01VAY0105002",  #    01/01/1805
        "01LNN0107002",  #    01/01/1807
        "01MJA0107011",  #    01/01/1807
        # 2012 Birthdays unclear how to correct
        "09GAA0487001",  #    09/04/1487
        # 2011 birthday that unclear how to correct
        "01QLO0105000",  #   01/01/1805
        "01KAA0106007",  #   01/01/1806
        "01LSH0108007",  #   01/01/1808
        "01KJN0111026",  #   01/01/1811
        "01AMN0108001",  #   01/01/1808
        # super old - clearly incorrect birthday
        # generated with:
        # print(voters[voters['age']>118].reset_index()[['Voter ID Number', 'Date of Birth']])  # noqa: E501
        "01ORA0112003",  #   01/01/1812
        "01CAY0112006",  #   01/01/1812
        "01EJD0112000",  #   01/01/1812
        "01FCA0112004",  #   01/01/1812
        "01GPA0112002",  #   01/01/1812
        "01SNE0112002",  #   01/01/1812
        "01GAA0112013",  #   01/01/1812
        "01WJE0112006",  #   01/01/1812
        "01LMH0112001",  #   01/01/1812
        "01MEY0112005",  #   01/01/1812
        "01FPK0112000",  #   01/01/1812
        "01IFA0112001",  #   01/01/1812
        "01LSE0112003",  #   01/01/1812
        "01RSH0112002",  #   01/01/1812
        "01CKN0113009",  #   01/01/1813
        "01AAA0112016",  #   01/01/1812
    ]
    vlist = vlist.drop(drop_ids, errors="ignore")
    history = history.drop(drop_ids, errors="ignore")

    # 04WDA0180001 in 2011
    # 12GDA0186001
    # 01DML1591001
    # 08WJB0481002
    # I modified the birth date year from 0980 to 1980
    # if "04WDA0180001" in vlist:
    #     # correcting a date entered as 0980
    #     print('here?')
    #     vlist["04WDA0180001"]["Date of Birth"] = "04/01/1980"

    # add 12 hours so that people turning 18 on election day
    # get calculated as being 18, not 17
    birth_dates = pd.to_datetime(vlist["Date of Birth"])
    # extract from the file
    # this will break if multiple elec in same year
    elec_date = pd.to_datetime(history["Election Date"].iloc[0])

    # # check that this is actually correct ideally
    # subtract (1-1/365) to make it so people turning 18 on election day count as 18
    age = np.ceil(
        (elec_date - birth_dates) / timedelta(days=365.2425) - (1 - 1 / 365)
    ).astype(int)
    vlist["age"] = age
    vlist["voted"] = False
    vlist.loc[vlist.index.intersection(history.index), "voted"] = True
    return vlist


def load_full_dataset(data_folder):
    data_folder = Path(data_folder)
    voters_2022 = load_year(
        data_folder / "11-8-22 Voter History 49ANP_269498.txt",
        data_folder / "49VOT_267488 nov 2022 voting list.txt",
    )
    voters_2020 = load_year(
        data_folder / "11-3-20 Voter History 49ANP_225530.txt",
        data_folder / "49VOT_224084 november 2020 election.txt",
    )
    voters_2018 = load_year(
        data_folder / "11-6-18 Voter History 49ANP_162771.txt",
        data_folder / "49VOT_162354 - Nov 6 2018 Election.txt",
    )
    voters_2016 = load_year(
        data_folder / "11-8-16 Voter History 49ANP_140283.txt",
        data_folder / "49VOT_139226 - Nov 8 2016.txt",
    )
    voters_2014 = load_year(
        data_folder / "11-4-2014 State Election 49ANP_120872.txt",
        data_folder / "49VOT_120372 - nov 4 2014.txt",
    )
    voters_2012 = load_year(
        data_folder / "11.6.2012 StatePres 49ANP_103892.txt",
        data_folder / "49VOT_103340 Nov 2012 election.txt",
    )
    voters_2021 = load_year(
        data_folder / "11-2-21 Voter History 49ANP_239643.txt",
        data_folder / "49VOT_238743 Nov 2021 election.txt",
    )
    voters_2019 = load_year(
        data_folder / "11-5-19 Voter History 49ANP_202374.txt",
        data_folder / "49VOT_199524 - Nov 2019 election.txt",
    )
    voters_2017 = load_year(
        data_folder / "11.7.17 Voter History 49ANP_150723.txt",
        data_folder / "49VOT_150177 - nov 7 2017.txt",
    )
    voters_2015 = load_year(
        data_folder / "11.3.15 Voter History 49ANP_129528.txt",
        data_folder / "49VOT_128567 - Nov 3, 2015.txt",
    )
    voters_2013 = load_year(
        data_folder / "11.5.13 Municipal Election 49ANP_112159.txt",
        data_folder / "49VOT_111500 - nov 5, 2013.txt",
    )
    voters_2011 = load_year(
        data_folder / "11.8.2011 Voter History 49ANP_91255.txt",
        data_folder / "49VOT_90931 Nov 2011 election.txt",
    )

    col_order = [
        "Last Name",
        "Middle Name",
        "First Name",
        "voted",
        "age",
        "Date of Birth",
        "Date of Registration",
        "Residential Address Street Number",
        "Residential Address Street Name",
        "univ_housing_name",
        "Residential Address Street Suffix",
        "Residential Address Apartment Number",
        "Residential Address Zip Code",
        # 'Mailing Address - Street Number and Name',
        # 'Mailing Address - Apartment Number',
        # 'Mailing Address - City or Town',
        # 'Mailing Address - State',
        # 'Mailing Address - Zip Code',
        "Gender F/M",
        "Voter Status",
        "Party Affiliation",
        "Ward Number",
        "Precinct Number",
        "Congressional District Number",
        "Senatorial District Number",
        "State Representative District",
        # 'Unnamed: 26',
        # 'Unnamed: 25',
        #  'Record Sequence Number',
        # 'Title',
    ]
    voters = pd.concat(
        [
            voters_2011,
            voters_2012,
            voters_2013,
            voters_2014,
            voters_2015,
            voters_2016,
            voters_2017,
            voters_2018,
            voters_2019,
            voters_2020,
            voters_2021,
            voters_2022,
        ],
        keys=np.arange(2011, 2023),
    )

    # add a university housing name column
    # makes it easier to do things like groupby for MIT dorms
    voters["univ_housing_name"] = "NA"

    voters = voters[col_order]
    voters.index = voters.index.set_names(["year", "Voter ID Number"])
    return voters


def _group_turnout(df: pd.DataFrame, key: str, bin_size: int) -> pd.DataFrame:
    """
    Convert the output of *turn to turnout by age group.

    """

    grouped = df.reset_index()
    min_ = grouped[key].min()
    max_ = grouped[key].max()
    groups = pd.cut(grouped[key], np.arange(min_, max_, bin_size), include_lowest=True)
    group_key = f"{key}_group"
    grouped[group_key] = groups
    grouped = (
        grouped.groupby(["year", group_key], observed=True)
        .sum()
        .sort_index()
        .drop(key, axis=1)
        .reset_index()
    )
    mid_points = [g.mid for g in grouped[group_key]]
    if key == "age":
        # Corrects for the lowerst midpoint being 19.9995 due to
        # include lowest
        mid_points = np.ceil(mid_points).astype(int)

    grouped["mid_points"] = mid_points  # convenience for plotting down the line
    # transforming the intervals into strings for easy using the multiindex
    # this can't be the best way to do this :(
    # this is lowkey awful
    grouped[group_key] = [
        f"{int(np.round(g.left))}-{int(g.right)}" for g in grouped[group_key]
    ]

    grouped.index = pd.MultiIndex.from_frame(grouped[["year", group_key]])
    grouped = grouped.drop(["year", group_key], axis=1)
    grouped["turnout"] = grouped["voted"] / grouped["registered"]
    return grouped


def turnout_by_year_key(df, key, binning: int = None):
    """
    Calculate turnout per year based on the variable *key*.

    Parameters
    ----------
    df : pd.DataFrame
        Expected to have an outer (multi)index of *year*
    key : str
        The column to use for value_counts. e.g. "age"
    binning : int
        If the *key* is numerical then group it into bins of this size.
    Returns
    -------
    pd.DataFrame
    """

    def _process_year(df):
        voted_counts = df[df["voted"]][key].value_counts().sort_index()
        reg_counts = df[key].value_counts().sort_index()
        df = pd.DataFrame({"voted": voted_counts, "registered": reg_counts})
        return df.fillna(0).astype(int)

    years = df.index.unique(level=0)
    out = pd.concat([_process_year(df.loc[year]) for year in years], keys=years)
    out.index = out.index.set_names(["year", key])
    out["turnout"] = out["voted"] / out["registered"]
    if binning is not None:
        out = _group_turnout(out, key, binning)
    return out
