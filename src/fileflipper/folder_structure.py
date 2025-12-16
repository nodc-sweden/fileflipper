class FolderStructure:

    def __init__(self,
                 data_type: str | None = None,
                 deliverer: str | None = None,
                 year: int | None = None,
                 orderer: str | None = None,
                 ) -> None:
        self._data_type = data_type
        self._deliverer = deliverer
        self._year = year
        self._orderer = orderer

    @property
    def data_type(self) -> str:
        return self._data_type

    @data_type.setter
    def data_type(self, data_type: str) -> None:
        if not isinstance(data_type, str):
            raise TypeError(f"Data type must by of type str: {type(data_type)} was given!")
        self._data_type = data_type

    @property
    def deliverer(self) -> str:
        return self._deliverer

    @property
    def year(self) -> int:
        return self._year

    @property
    def orderer(self) -> str:
        return self._orderer

    @property
    def folder_name(self) -> str:
        return self._data_type

    def __repr__(self):
        return (f"FolderStructure with data_type={self._data_type} and deliverer={self._deliverer} and "
                f"year={self._year} and orderer={self._orderer}")


if __name__ == "__main__":
    fs = FolderStructure(
        "phytoplankton",
        "SMHI",
        2000,
        "OLST"
    )

    fss = FolderStructure(
        "fyskem",
        "SMHI",
        2001,
        "YLST"
    )
