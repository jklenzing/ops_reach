# -*- coding: utf-8 -*-
"""Provides metadata specific routines for REACH data."""

import datetime as dt
import numpy as np

import pysat

ackn_str = ' '.join(('The development of the CDF files was supported by the SPI',
                     'Goddard HISFM 2022. The success of the REACH project is',
                     'owed to a long line of people who have contributed to it',
                     'over the many years of development. The REACH hardware',
                     'team in The Aerospace Corporation’s xLab organization',
                     'included Paul Carranza, Sue Crain, Bill Crain, Andrew Hsu,',
                     'Brian McCarthy, John McHale, Can Nguyen, Mario Perez, Deb',
                     'Salvaggio, and Gerrit Sorensen, all critical to designing',
                     'and fabricating the first 18 of the 32 REACH pods. Millennium',
                     'Engineering and Integration (MEI) manufactured the remaining',
                     '14 pods. Doug Holker was instrumental in nearly all facets of',
                     'REACH development, outreach, support, endorsement and project',
                     'management for the entirety of the project’s lifetime. The',
                     'REACH project was led in chronological order by the following',
                     'USAF Program Managers: Capt Dan Kimmich, Lt Garrett Ellis, Lt',
                     'Justin Shimasaki, Capt Sean Quintana, Capt Felix Abeyta, Lt',
                     'Kurt Mann, Maj James Crane, Capt Omar Manning, Lt Zach Morley,',
                     'Capt Scott Day, Lt Zeesha Braslawsce, and Lt Ryan Francies. This',
                     'list reflects their ranks at the time of involvement. Recent',
                     'management is possible through the SMC/Development Corp program',
                     'office support Pete Cunningham. Data transport is provided by',
                     'Iridium, L3Harris, and data processing of the Level 0 files is',
                     'performed by Robin Barnes and supported by Tom Sotirelis and',
                     'Mike Kelly at the Johns Hopkins Applied Physics Laboratory.',
                     'Alexa Halford, now of NASA Goddard Space Flight Center,',
                     'prototyped many higher-level REACH data products and performed',
                     'intra-calibration of the dosimeters.'))


def scrub_l1b(data):
    """Make data labels compatible with SPASE and pysat.

    Parameters
    ----------
    data : pandas.Dataframe()
        Metadata object containing the default metadata loaded from the csv files.

    Returns
    -------
    data : pandas.Datafram()
        Replacement data object with compatible variable names.

    """

    # Rename date variables
    data = data.rename(columns={'YYYY': 'year', 'mm': 'month', 'DD': 'day',
                                'HH': 'hour', 'MM': 'minute',
                                'SEC': 'seconds', 'MJD': 'mjd', 'DoY': 'doy',
                                'VID': 'vid', 'ALT km': 'altitude',
                                'LAT deg': 'latitude', 'LON deg': 'longitude',
                                'GEO_X RE': 'geo_x', 'GEO_Y RE': 'geo_y',
                                'GEO_Z RE': 'geo_z', 'GEI_X RE': 'gei_x',
                                'GEI_Y RE': 'gei_y', 'GEI_Z RE': 'gei_z',
                                'DOSE1 rad/s': 'dose1',
                                'PROT FLUX1 #/cm^2/sr/s': 'proton_flux1',
                                'ELEC FLUX1 #/cm^2/sr/s': 'electron_flux1',
                                'SPECIES1': 'species1', 'DOSE2 rad/s': 'dose2',
                                'PROT FLUX2 #/cm^2/sr/s': 'proton_flux2',
                                'ELEC FLUX2 #/cm^2/sr/s': 'electron_flux2',
                                'SPECIES2': 'species2',
                                'HK Temperature deg C': 'hk_temperature',
                                'HK 15V Monitor': 'hk_15v_monitor',
                                'HK 5V Monitor': 'hk_5v_monitor',
                                'HK 3.3V Monitor': 'hk_3_3v_monitor',
                                'Lm RE': 'lm', 'Inv_Lat deg': 'inverse_lat',
                                'Blocal nT': 'blocal', 'Bmin nT': 'bmin',
                                'MLT hr': 'mlt', 'K sqrt(G)RE': 'k_sqrt',
                                'hmin km': 'hmin', 'Alpha deg': 'alpha',
                                'Alpha Eq deg': 'alpha_eq',
                                'Region Code': 'region_code',
                                'Orbit Status': 'orbit_status',
                                'Flag': 'flag'})

    # Now we make our Epoch variable
    Epoch = np.array([dt.datetime(data['year'][i], data['month'][i],
                                  data['day'][i], data['hour'][i],
                                  data['minute'][i], data['seconds'][i])
                     for i in range(len(data))])
    data.index = Epoch

    return data


def generate_header(inst_id, epoch):
    """Generate the meta header info.

    Parameters
    ----------
    inst_id : str
        The VID of the associated dataset.
    epoch : dt.datetime
        The epoch of the datafile.  Corresponds to the first data point.

    Returns
    -------
    header : dict
        A dictionary compatible with the pysat.meta_header format.  Top-level
        metadata for the file.

    """

    header = {'Project': 'The Aerospace Corporation',
              'Discipline': 'Space Physics>Magnetospheric Science, Space Weather',
              'Data_type': 'pre>Preliminary',
              'Descriptor': ' '.join(('reach-v3', inst_id, '>, The Responsive',
                                      'Environmental Assessment Commercially',
                                      'Hosted (REACH)  version-3 Data for,'
                                      'vehical ID ', inst_id)),
              'TITLE': 'Responsive Environmental Assessment Commercially Hosted',
              'TEXT': ' '.join(('The Responsive Environmental Assessment Commercially',
                                'Hosted (REACH) constellation is collection of 32 small',
                                'sensors hosted on six orbital planes of the',
                                'Iridium-Next space vehicles in low earth orbit.',
                                'Each sensor contains two micro-dosimeters sensitive',
                                'to the passage of charged particles from the Earth’s',
                                'radiation belts. There are six distinct dosimeter',
                                'types spread among the 64 individual sensors, which',
                                'are unique in shielding and electronic threshold. When',
                                'taken together, this effectively enables a high',
                                'time-cadence measurement of protons and electrons in',
                                'six integral energy channels over the entire globe.')),
              'Source_name': ' '.join(('reach>The Responsive Environmental Assessment',
                                       'Commercially Hosted, satellite id ', inst_id)),
              'Logical_source': ''.join(('reach.', epoch.strftime('%Y%m%d'),
                                         '.vid-', inst_id, '.l1b.v3')),
              'File_naming_convention': 'source_date_vehicalID_descriptor',
              'Data_version': '03',
              'Software_version': 'l1b',
              'PI_name': 'Joe Mazur (joseph.e.mazur@aero.or)',
              'PI_affiliation': 'The Aerospace Corporation',
              'Data_Curator': 'Timothy B. Guild (Timothy.B.Guild@aero.org)',
              'DC_afiliation': 'The Aerospace Corporation',
              'Instrument_type': 'Particles (space)',
              'Mission_group': ' '.join(('The Responsive Environmental Assessment',
                                         'Commercially Hosted (REACH)')),
              'Time_resolution': '5 seconds',
              'Rules_of_use': ''.join(('See Usage Guidelines at: https://',
                                       'zenodo.org/record/6423507#.YmMqcfPMLCU')),
              'Generated_by': ' '.join(('csv files generated at The Aerosapce',
                                        'Corporation, CDF files generated by Alexa',
                                        'Halford at NASA Goddard Space Flight Center')),
              'Generation_date': dt.datetime.today().strftime('%Y-%m-%d'),
              'Generation_datetime': dt.datetime.today().isoformat(),
              'Acknowledgement': ackn_str,
              'LINK_TEXT': 'REACH csv files are avalible at ',
              'LINK_TITLE': 'REACH data ',
              'HTTP_LINK': 'https://zenodo.org/record/6423507#.YmMwUfPMLCV'}

    return header


def generate_metadata(header_data):
    """Generate metadata object for reach l1b data compatible with SPASE and pysat.

    Parameters
    ----------
    inst_id : str
        The VID of the associated dataset.
    epoch : dt.datetime
        The epoch of the datafile.  Corresponds to the first data point.

    Returns
    -------
    metadata : pandas.Dataframe()
        Contains data compatible with SPASE standards to initialize pysat.Meta.

    """

    # Create required metadata values
    meta = pysat.Meta(header_data=header_data)

    meta['mjd'] = {meta.labels.units: '???',
                   meta.labels.min_val: 0.0,
                   meta.labels.max_val: np.nan}
    meta['year'] = {meta.labels.units: 'years',
                    meta.labels.min_val: 0,
                    meta.labels.max_val: np.inf}
    meta['month'] = {meta.labels.units: 'months',
                     meta.labels.min_val: 0,
                     meta.labels.max_val: 12}
    meta['day'] = {meta.labels.units: 'days',
                   meta.labels.min_val: 0,
                   meta.labels.max_val: 31}
    meta['hour'] = {meta.labels.units: 'hours',
                    meta.labels.min_val: 0.0,
                    meta.labels.max_val: 24.0}
    meta['minute'] = {meta.labels.units: 'minutes',
                      meta.labels.min_val: 0.0,
                      meta.labels.max_val: 60.0}
    meta['seconds'] = {meta.labels.units: 'seconds',
                       meta.labels.min_val: 0.0,
                       meta.labels.max_val: 60.0}
    meta['doy'] = {meta.labels.units: 'days',
                   meta.labels.min_val: 0,
                   meta.labels.max_val: 366}
    meta['vid'] = {meta.labels.units: '???',
                   meta.labels.min_val: 0.0,
                   meta.labels.max_val: np.nan}
    meta['altitude'] = {meta.labels.units: 'km',
                        meta.labels.min_val: 0.0,
                        meta.labels.max_val: np.inf}
    meta['latitude'] = {meta.labels.units: 'degrees',
                        meta.labels.min_val: -90.0,
                        meta.labels.max_val: 90.0}
    meta['longitude'] = {meta.labels.units: 'degrees',
                         meta.labels.min_val: 0.0,
                         meta.labels.max_val: 360.0}
    meta['geo_x'] = {meta.labels.units: 'RE',
                     meta.labels.min_val: -2.0,
                     meta.labels.max_val: 2.0}
    meta['geo_y'] = {meta.labels.units: 'RE',
                     meta.labels.min_val: -2.0,
                     meta.labels.max_val: 2.0}
    meta['geo_z'] = {meta.labels.units: 'RE',
                     meta.labels.min_val: -2.0,
                     meta.labels.max_val: 2.0}
    meta['gei_x'] = {meta.labels.units: 'RE',
                     meta.labels.min_val: -2.0,
                     meta.labels.max_val: 2.0}
    meta['gei_y'] = {meta.labels.units: 'RE',
                     meta.labels.min_val: -2.0,
                     meta.labels.max_val: 2.0}
    meta['gei_z'] = {meta.labels.units: 'RE',
                     meta.labels.min_val: -2.0,
                     meta.labels.max_val: 2.0}
    meta['dose1'] = {meta.labels.units: 'rad/s',
                     meta.labels.min_val: 0.0,
                     meta.labels.max_val: np.inf}
    meta['proton_flux1'] = {meta.labels.units: '#/cm^2/sr/s',
                            meta.labels.min_val: 0.0,
                            meta.labels.max_val: np.inf}
    meta['electron_flux1'] = {meta.labels.units: '#/cm^2/sr/s',
                              meta.labels.min_val: 0.0,
                              meta.labels.max_val: np.inf}
    meta['species1'] = {meta.labels.units: '???',
                        meta.labels.min_val: 0.0,
                        meta.labels.max_val: np.nan}
    meta['dose2'] = {meta.labels.units: 'rad/s',
                     meta.labels.min_val: 0.0,
                     meta.labels.max_val: np.inf}
    meta['proton_flux2'] = {meta.labels.units: '#/cm^2/sr/s',
                            meta.labels.min_val: 0.0,
                            meta.labels.max_val: np.inf}
    meta['electron_flux2'] = {meta.labels.units: '#/cm^2/sr/s',
                              meta.labels.min_val: 0.0,
                              meta.labels.max_val: np.inf}
    meta['species2'] = {meta.labels.units: '???',
                        meta.labels.min_val: 0.0,
                        meta.labels.max_val: np.nan}
    meta['hk_temperature'] = {meta.labels.units: 'degrees C',
                              meta.labels.min_val: 0.0,
                              meta.labels.max_val: 20.0}
    meta['hk_15v_monitor'] = {meta.labels.units: '???',
                              meta.labels.min_val: 0.0,
                              meta.labels.max_val: np.nan}
    meta['hk_5v_monitor'] = {meta.labels.units: '???',
                             meta.labels.min_val: 0.0,
                             meta.labels.max_val: np.nan}
    meta['hk_3_3v_monitor'] = {meta.labels.units: '???',
                               meta.labels.min_val: 0.0,
                               meta.labels.max_val: np.nan}
    meta['lm'] = {meta.labels.units: 'RE',
                  meta.labels.min_val: 0.0,
                  meta.labels.max_val: 30.0}
    meta['inverse_lat'] = {meta.labels.units: 'deg',
                           meta.labels.min_val: 0.0,
                           meta.labels.max_val: np.nan}
    meta['blocal'] = {meta.labels.units: 'nT',
                      meta.labels.min_val: 0.0,
                      meta.labels.max_val: np.nan}
    meta['bmin'] = {meta.labels.units: 'nT',
                    meta.labels.min_val: 0.0,
                    meta.labels.max_val: np.nan}
    meta['mlt'] = {meta.labels.units: 'hours',
                   meta.labels.min_val: 0.0,
                   meta.labels.max_val: np.nan}
    meta['k_sqrt'] = {meta.labels.units: 'RE',
                      meta.labels.min_val: 0.0,
                      meta.labels.max_val: np.nan}
    meta['hmin'] = {meta.labels.units: 'km',
                    meta.labels.min_val: 0.0,
                    meta.labels.max_val: np.nan}
    meta['alpha'] = {meta.labels.units: 'deg',
                     meta.labels.min_val: 0.0,
                     meta.labels.max_val: np.nan}
    meta['alpha_eq'] = {meta.labels.units: '???',
                        meta.labels.min_val: 0.0,
                        meta.labels.max_val: np.nan}
    meta['region_code'] = {meta.labels.units: '???',
                           meta.labels.min_val: 0.0,
                           meta.labels.max_val: np.nan}
    meta['orbit_status'] = {meta.labels.units: '???',
                            meta.labels.min_val: 0.0,
                            meta.labels.max_val: np.nan}
    meta['flag'] = {meta.labels.units: '???',
                    meta.labels.min_val: 0.0,
                    meta.labels.max_val: np.nan}

    return meta
