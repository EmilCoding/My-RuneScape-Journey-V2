from rshisttools.paths import COMPLETED_FOLDERS
from rshisttools.dates import GAME_RELEASE_DAY, current_ingame_date


# ============================================================================================================================ #
# COMPLETED_FOLDERS tests                                                                                                      #
# ============================================================================================================================ #
def test_keys_of_completed_folders_are_up_to_date():
    """Test of all the year up to and including in game dates
    are present in the ´COMPLETED_FOLDERS´ dictionary.
    """
    missing_years = [
        year
        for year in range(GAME_RELEASE_DAY.year, current_ingame_date().year + 1)
        if year not in COMPLETED_FOLDERS
    ]
    assert not missing_years, f"Years {missing_years} are missing in COMPLETED_FOLDERS."


def test_path_match_keys():
    """Test if all keys match the folder names in ´COMPLETED_FOLDERS´ dictionary"""
    failed_key_name_match = [
        year
        for year, path in COMPLETED_FOLDERS.items()
        if year != int(path.name)
    ]
    assert not failed_key_name_match, f"Years {failed_key_name_match} have a mismatch in key and foldername."


def test_path_exists_in_completed_folders():
    """Test if all paths exists in ´COMPLETED_FOLDERS´ dictionary"""
    failed_keys = [
        year
        for year, path in COMPLETED_FOLDERS.items()
        if not path.exists()
    ]
    assert not failed_keys, f"Path of year {failed_keys} does not exists"
