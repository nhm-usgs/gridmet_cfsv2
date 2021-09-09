# -*- coding: utf-8 -*-
import datetime
import re
import urllib
from pathlib import Path
import itertools
import xarray as xr
import glob


class Gridmet():
    SCHEME = 'http'
    NETLOC = 'thredds.northwestknowledge.net:8080'
    SOURCE = 'http://thredds.northwestknowledge.net:8080'
    PATH = {
        'daily_maximum_temperature': '/thredds/dodsC/NWCSC_INTEGRATED_SCENARIOS_ALL_CLIMATE/cfsv2_metdata_90day/',
        'daily_minimum_temperature': '/thredds/dodsC/NWCSC_INTEGRATED_SCENARIOS_ALL_CLIMATE/cfsv2_metdata_90day/',
        'precipitation_amount': '/thredds/dodsC/NWCSC_INTEGRATED_SCENARIOS_ALL_CLIMATE/cfsv2_metdata_90day/',
        'wind_speed': '/thredds/dodsC/NWCSC_INTEGRATED_SCENARIOS_ALL_CLIMATE/cfsv2_metdata_90day/',
        'specific_humidity': '/thredds/dodsC/NWCSC_INTEGRATED_SCENARIOS_ALL_CLIMATE/cfsv2_metdata_90day/',
        'surface_downwelling_shortwave_flux_in_air': '/thredds/dodsC/NWCSC_INTEGRATED_SCENARIOS_ALL_CLIMATE'
        '/cfsv2_metdata_90day/'
    }
    NCF_NAME = {
        'daily_maximum_temperature': 'cfsv2_metdata_forecast_tmmx_daily',
        'daily_minimum_temperature': 'cfsv2_metdata_forecast_tmmn_daily',
        'precipitation_amount': 'cfsv2_metdata_forecast_pr_daily',
        'wind_speed': 'cfsv2_metdata_forecast_vs_daily',
        'specific_humidity': 'cfsv2_metdata_forecast_sph_daily',
        'surface_downwelling_shortwave_flux_in_air': 'cfsv2_metdata_forecast_srad_daily'
    }
    ENS_TYPE = {
        0: 'Ensemble Day 0',
        1: 'Ensemble Day 1',
        2: 'Ensemble Day 2',
        3: 'Ensemble All',
        4: 'Ensemble Median'
    }

    def __init__(self, lazy=True, cache_dir=None, type=0):

        self._start_date = None
        self._end_date = None
        self.type = type

        if cache_dir is None:
            cache_dir = Path('~/.gridmet')
        self._cache_dir = Path(cache_dir).expanduser().resolve()

        self._dataset = None
        self._ds_tmax = None
        self._ds_tmin = None
        self._ds_prcp = None
        self._ds_sph = None
        self._ds_ws = None
        self._ds_srad = None

        if not lazy:
            for name in self.PATH:
                self._lazy_load(name)

        # self.dt = 1.0
        # self.time = 0.0
        # self.end = float(self._delta.days + 1)

    @staticmethod
    def clear_cache(cache_dir=None):
        for fname in Gridmet.list_cache(cache_dir=cache_dir):
            fname.unlink()

    @staticmethod
    def list_cache(cache_dir=None, var=None):
        # if var not in ['tmax', 'tmin', 'prcp']

        if cache_dir is None:
            cache_dir = Path('~/.gridmet')
        cache_dir = Path(cache_dir).expanduser().resolve()

        pattern = r'(?P<var>[a-z_]*)_(?P<start>[0-9\-]*)_(?P<end>[0-9\-]*)\.nc'

        cached_files = []
        for fname in [p.name for p in cache_dir.glob('*.nc')]:
            match = re.match(pattern, fname)
            if match and match.group('var') in Gridmet.PATH:
                try:
                    datetime.date.fromisoformat(match.group('start'))
                    datetime.date.fromisoformat(match.group('end'))
                except ValueError:
                    pass
                else:
                    cached_files.append(cache_dir / fname)

        return cached_files

    @staticmethod
    def datetime_or_yesterday(val):
        if val is None:
            return datetime.date.today() - datetime.timedelta(days=1)
        elif isinstance(val, str):
            return datetime.date.fromisoformat(val)
        else:
            return val

    # @classmethod
    # def from_today(cls, days, lazy=True):
    #     if days <= 0:
    #         raise ValueError('number of days must be positive ({0})'.format(days))

    #     end_date = datetime.date.today()
    #     start_date = end_date - datetime.timedelta(days=days)

    #     return cls(start_date, end_date, lazy=lazy)

    @property
    def cache_dir(self):
        return self._cache_dir

    @property
    def start_date(self):
        return str(self._start_date)

    @property
    def end_date(self):
        return str(self._end_date)

    @property
    def dataset(self):
        return self._dataset

    def _fetch_and_open(self, name):
        self._cache_dir.mkdir(exist_ok=True)
        return Gridmet.fetch_var(
                name,
                self._cache_dir,
                self.type
            )

    def _lazy_load(self, name):
        if name == 'daily_maximum_temperature':
            if self._ds_tmax is None:
                self._ds_tmax = self._fetch_and_open(name)
                return self._ds_tmax
            else:
                return self._ds_tmax
        elif name == 'daily_minimum_temperature':
            if self._ds_tmin is None:
                self._ds_tmin = self._fetch_and_open(name)
                return self._ds_tmin
            else:
                return self._ds_tmin
        elif name == 'precipitation_amount':
            if self._ds_prcp is None:
                self._ds_prcp = self._fetch_and_open(name)
                return self._ds_prcp
            else:
                return self._ds_prcp
        elif name == 'wind_speed':
            if self._ds_ws is None:
                self._ds_ws = self._fetch_and_open(name)
                return self._ds_ws
            else:
                return self._ds_ws
        elif name == 'specific_humidity':
            if self._ds_sph is None:
                self._ds_sph = self._fetch_and_open(name)
                return self._ds_sph
            else:
                return self._ds_sph
        elif name == 'surface_downwelling_shortwave_flux_in_air':
            if self._ds_srad is None:
                self._ds_srad = self._fetch_and_open(name)
                return self._ds_srad
            else:
                return self._ds_srad

    @property
    def tmax(self) -> xr:
        tname = 'daily_maximum_temperature'
        ds = self._lazy_load(tname)
        return ds

    @property
    def tmin(self):
        tname = 'daily_minimum_temperature'
        ds = self._lazy_load(tname)
        return ds

    @property
    def prcp(self):
        tname = 'precipitation_amount'
        ds = self._lazy_load(tname)
        return ds

    @property
    def specific_humidity(self):
        return self._lazy_load('specific_humidity')

    @property
    def wind_speed(self):
        return self._lazy_load('wind_speed')

    @property
    def srad(self):
        return self._lazy_load('surface_downwelling_shortwave_flux_in_air')

    @classmethod
    def fetch_var(cls, name, cache_dir, type):
        if name not in cls.PATH:
            raise ValueError(
                'name not understood ({0} not in {1})'.format(name, ', '.join(cls.PATH))
            )
        if type not in cls.ENS_TYPE:
            raise ValueError(
                f'The specified type {type} is not in {cls.ENS_TYPE}'
            )
        fcst = ('00', '06', '12', '18')
        ensb = ('1', '2', '3', '4')
        day = ('0', '1', '2')
        files = []
        if type == 4:
            fext = '_median.nc'
            dsname = cls.SOURCE + cls.PATH[name] + cls.NCF_NAME[name] + '.nc'

            # fname = cls.NCF_NAME[name] + fext

            # fobj = xr.open_dataset(dsname+'#fillmismatch', engine='netcdf4', mask_and_scale=True)
            # fobj.to_netcdf(cache_dir / fname)
            # fobj.close()
            # gname = str(cache_dir / (cls.NCF_NAME[name] + '_median.nc'))
            # # paths = glob.glob(gname)

            return xr.open_dataset(dsname+'#fillmismatch')

        elif type == 3:
            file_list = []
            for index, (tday, tensb, tfcst) in enumerate(itertools.product(day, ensb, fcst)):
                # print(tfcst,tensb, tday)
                fext = f'_{tfcst}_{tensb}_{tday}.nc'
                # fext2 = f'_{tfcst}_{tensb}_{tday}_{index}.nc'
                dsname = cls.SOURCE + cls.PATH[name] + cls.NCF_NAME[name] + fext+'#fillmismatch'
                file_list.append(dsname)
            #     fname = cls.NCF_NAME[name] + fext2

            #     fobj = xr.open_dataset(dsname+'#fillmismatch', engine='netcdf4', mask_and_scale=True)
            #     fobj.to_netcdf(cache_dir / fname)
            #     fobj.close()
            #     fullname = cache_dir / fname
            #     files.append(fullname)
            # gname = str(cache_dir / (cls.NCF_NAME[name] + '_[0-9]*.nc'))
            # # paths = sorted(glob.glob(gname))

            # print(files)
            return xr.open_mfdataset(file_list, combine='nested', concat_dim='time', parallel=True)

        elif type in [0, 1, 2]:
            file_list = []
            for tfcst, tensb in itertools.product(fcst, ensb):
                tday = int(type)
                fext = f'_{tfcst}_{tensb}_{tday}.nc'
                dsname = cls.SOURCE + cls.PATH[name] + cls.NCF_NAME[name] + fext+'#fillmismatch'
                file_list.append(dsname)
            # print(file_list)
            return xr.open_mfdataset(file_list, combine='nested', concat_dim='time', parallel=True)

    @classmethod
    def data_url(cls, name):
        return urllib.parse.urlunparse(
            (cls.SCHEME, cls.NETLOC, cls.PATH[name], '', '', '')
        )

    def update(self):
        self.time += self.dt
