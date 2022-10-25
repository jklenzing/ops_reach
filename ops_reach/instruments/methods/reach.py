# -*- coding: utf-8 -*-
"""Provides metadata specific routines for REACH data."""

import datetime as dt
import numpy as np
import os
import pandas as pds

import pysat

import ops_reach


ackn_str = ' '.join(('The development of the netCDF files was supported by the SPI',
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
    """Make data labels and epoch compatible with SPASE and pysat.

    Parameters
    ----------
    data : pandas.Dataframe()
        Metadata object containing the default metadata loaded from the csv files.

    Returns
    -------
    data : pandas.Datafram()
        Replacement data object with compatible variable names and epoch.

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
                                'Lm RE': 'lm', 'Inv_Lat deg': 'inv_lat',
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
              'Data_product': 'l1b',
              'Data_version': '03',
              'PI_name': 'Joe Mazur (joseph.e.mazur@aero.org)',
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
                                        'Corporation, netCDF files generated by Alexa',
                                        'Halford at NASA Goddard Space Flight Center')),
              'Generation_date': dt.datetime.today().strftime('%Y-%m-%d'),
              'Generation_datetime': dt.datetime.today().isoformat(),
              'Acknowledgement': ackn_str,
              'LINK_TEXT': 'REACH csv files are avalible at ',
              'LINK_TITLE': 'REACH data ',
              'HTTP_LINK': 'https://zenodo.org/record/6423507#.YmMwUfPMLCV'}

    # Extract info from pod serial numbers
    path = os.path.join(ops_reach.__here__, 'instruments', 'methods',
                        'pod_serial_numbers.csv')
    pods = pds.read_csv(path)
    info = pods[pods['Hosted payload number (HPL)'] == int(inst_id)]
    for key in info.keys():
        header[key] = info[key].values[0]

    return header


def generate_metadata(header_data):
    """Generate metadata object for reach l1b data compatible with SPASE and pysat.

    Parameters
    ----------
    header_data : dict
        A dictionary compatible with the pysat.meta_header format.  Required to
        properly initialize metadata.

    Returns
    -------
    metadata : pandas.Dataframe()
        Contains data compatible with SPASE standards to initialize pysat.Meta.

    """

    # Create required metadata values
    meta = pysat.Meta(header_data=header_data)

    meta['mjd'] = {meta.labels.name: 'Modified Julian Day',
                   meta.labels.units: 'days',
                   meta.labels.min_val: 57754.0,
                   meta.labels.max_val: 80754.0}
    meta['year'] = {meta.labels.units: 'years',
                    meta.labels.min_val: 2017.0,
                    meta.labels.max_val: 2079.0}
    meta['month'] = {meta.labels.units: 'months',
                     meta.labels.min_val: 0.0,
                     meta.labels.max_val: 12.0}
    meta['day'] = {meta.labels.units: 'days',
                   meta.labels.min_val: 0.0,
                   meta.labels.max_val: 31.0}
    meta['hour'] = {meta.labels.units: 'hours',
                    meta.labels.min_val: 0.0,
                    meta.labels.max_val: 24.0}
    meta['minute'] = {meta.labels.units: 'minutes',
                      meta.labels.min_val: 0.0,
                      meta.labels.max_val: 60.0}
    meta['seconds'] = {meta.labels.units: 'seconds',
                       meta.labels.min_val: 0.0,
                       meta.labels.max_val: 60.0}
    meta['doy'] = {meta.labels.name: 'Day of Year',
                   meta.labels.units: 'days',
                   meta.labels.min_val: 0.0,
                   meta.labels.max_val: 366.0}
    meta['vid'] = {meta.labels.name: 'REACH Vehicle Identifier',
                   meta.labels.units: 'unitless',
                   meta.labels.min_val: 0.0,
                   meta.labels.max_val: np.nan}
    meta['altitude'] = {meta.labels.name: 'Geodetic Altitude',
                        meta.labels.units: 'km',
                        meta.labels.min_val: 750.0,
                        meta.labels.max_val: 850.0}
    meta['latitude'] = {meta.labels.name: 'Geodetic Latitude',
                        meta.labels.units: 'degrees',
                        meta.labels.min_val: -90.0,
                        meta.labels.max_val: 90.0}
    meta['longitude'] = {meta.labels.name: 'Geodetic Longitude',
                         meta.labels.units: 'degrees',
                         meta.labels.min_val: -180.0,
                         meta.labels.max_val: 180.0}
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
    meta['dose1'] = {meta.labels.name: 'Dose rate from Dosimeter 1',
                     meta.labels.units: 'rad/s',
                     meta.labels.min_val: 0.0,
                     meta.labels.max_val: np.nan}
    meta['proton_flux1'] = {meta.labels.name: 'Proton flux from bowtie',
                            meta.labels.units: '#/cm^2/sr/s',
                            meta.labels.min_val: 0.0,
                            meta.labels.max_val: np.nan}
    meta['electron_flux1'] = {meta.labels.name: 'Electron flux from bowtie',
                              meta.labels.units: '#/cm^2/sr/s',
                              meta.labels.min_val: 0.0,
                              meta.labels.max_val: np.nan}
    meta['species1'] = {meta.labels.name: 'Most probable species',
                        meta.labels.notes: '; '.join(('0 (not currently used)',
                                                      '1 – protons, 2-electrons',
                                                      'and 3-both / ambiguous')),
                        meta.labels.units: 'unitless',
                        meta.labels.min_val: 0,
                        meta.labels.max_val: 3}
    meta['dose2'] = {meta.labels.name: 'Dose rate from Dosimeter 2',
                     meta.labels.units: 'rad/s',
                     meta.labels.min_val: 0.0,
                     meta.labels.max_val: np.nan}
    meta['proton_flux2'] = {meta.labels.name: 'Proton flux from bowtie',
                            meta.labels.units: '#/cm^2/sr/s',
                            meta.labels.min_val: 0.0,
                            meta.labels.max_val: np.nan}
    meta['electron_flux2'] = {meta.labels.name: 'Electron flux from bowtie',
                              meta.labels.units: '#/cm^2/sr/s',
                              meta.labels.min_val: 0.0,
                              meta.labels.max_val: np.nan}
    meta['species2'] = {meta.labels.name: 'Most probable species',
                        meta.labels.notes: '; '.join(('0 (not currently used)',
                                                      '1 – protons, 2-electrons',
                                                      'and 3-both / ambiguous')),
                        meta.labels.units: 'unitless',
                        meta.labels.min_val: 0,
                        meta.labels.max_val: 3}
    meta['hk_temperature'] = {meta.labels.name: 'Housekeeping temperature',
                              meta.labels.units: 'degrees C',
                              meta.labels.min_val: 0.0,
                              meta.labels.max_val: 20.0}
    meta['hk_15v_monitor'] = {meta.labels.name: 'Housekeeping voltage 15V',
                              meta.labels.units: 'volts',
                              meta.labels.min_val: 0.0,
                              meta.labels.max_val: np.nan}
    meta['hk_5v_monitor'] = {meta.labels.name: 'Housekeeping voltage 5V',
                             meta.labels.units: 'volts',
                             meta.labels.min_val: 0.0,
                             meta.labels.max_val: np.nan}
    meta['hk_3_3v_monitor'] = {meta.labels.name: 'Housekeeping voltage 3.3V',
                               meta.labels.units: 'volts',
                               meta.labels.min_val: 0.0,
                               meta.labels.max_val: np.nan}
    meta['lm'] = {meta.labels.name: ' '.join(('McIlwain L-shell for locally',
                                              'mirroring particle')),
                  meta.labels.units: 'RE',
                  meta.labels.min_val: 0.0,
                  meta.labels.max_val: 30.0}
    meta['inv_lat'] = {meta.labels.name: ' '.join(('Invariant Latitude for',
                                                   'locally mirroring',
                                                   'particle')),
                       meta.labels.units: 'deg',
                       meta.labels.min_val: -90.0,
                       meta.labels.max_val: 90.0,
                       meta.labels.fill_val: -1.0e31}
    meta['blocal'] = {meta.labels.name: 'Local magnetic field at s/c',
                      meta.labels.units: 'nT',
                      meta.labels.min_val: 0.0,
                      meta.labels.max_val: np.nan}
    meta['bmin'] = {meta.labels.name: ' '.join(('Minimum magnetic field on',
                                                'field line intersecting',
                                                'spacecraft')),
                    meta.labels.units: 'nT',
                    meta.labels.min_val: 0.0,
                    meta.labels.max_val: np.nan}
    meta['mlt'] = {meta.labels.name: 'Magnetic local time',
                   meta.labels.units: 'hours',
                   meta.labels.min_val: 0.0,
                   meta.labels.max_val: 24.0}
    meta['k_sqrt'] = {meta.labels.units: 'RE',
                      meta.labels.min_val: 0.0,
                      meta.labels.max_val: np.nan}
    meta['hmin'] = {meta.labels.units: 'km',
                    meta.labels.min_val: 0.0,
                    meta.labels.max_val: np.nan}
    meta['alpha'] = {meta.labels.name: 'Local pitch angle',
                     meta.labels.units: 'deg',
                     meta.labels.min_val: 0.0,
                     meta.labels.max_val: 180.0}
    meta['alpha_eq'] = {meta.labels.name: 'Equatorial pitch angle',
                        meta.labels.units: 'deg',
                        meta.labels.min_val: 0.0,
                        meta.labels.max_val: 90.0,
                        meta.labels.fill_val: -1.0e31}
    meta['region_code'] = {
        meta.labels.notes: '; '.join(('-4: Southern Polar Cap',
                                      '-3: Outer Zone Untrapped',
                                      '-2: Slot Untrapped',
                                      '-1: Inner Zone Untrapped',
                                      '0: Unknown',
                                      '1: Inner Zone Trapped',
                                      '2: Slot Trapped',
                                      '3: Outer Zone Trapped',
                                      '4: Northern Polar Cap')),
        meta.labels.units: 'unitless',
        meta.labels.min_val: -4,
        meta.labels.max_val: 4}
    meta['orbit_status'] = {meta.labels.units: 'unitless',
                            meta.labels.notes: '1=Northbound; 2=Southbound',
                            meta.labels.min_val: 0.0,
                            meta.labels.max_val: np.nan}
    meta['flag'] = {
        meta.labels.notes: '; '.join((
            '-1: no data',
            '0: No known problems',
            '1: Test Mode',
            '2: Possible temperature-related self-counting in Dosimeter A.',
            '4: Possible temperature-related self-counting in Dosimeter B.',
            '8: Duplicate packets detected.',
            '16: Unknown issue with VID 163/Dosimeter B')),
        meta.labels.units: 'unitless',
        meta.labels.min_val: -1,
        meta.labels.max_val: 16}

    return meta
