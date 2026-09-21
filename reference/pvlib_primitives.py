def get_extra_radiation(datetime_or_doy, solar_constant=1366.1,
                        method='spencer', epoch_year=2014, **kwargs):
    """
    Determine extraterrestrial radiation from day of year.

    Specific references for each method are cited in the parameter descriptions
    below, while a more general discussion of the different models may also be
    found in [1]_ and [2]_.

    Parameters
    ----------
    datetime_or_doy : numeric, array, date, datetime, Timestamp, DatetimeIndex
        Day of year, array of days of year, or datetime-like object

    solar_constant : float, default 1366.1
        The solar constant. [Wm⁻²]

    method : string, default `spencer`
        The method by which the extraterrestrial radiation should be
        calculated. Options include: `pyephem`, `spencer` [3]_, `asce` [4]_,
        'nrel' [6]_.

    epoch_year : int, default 2014
        The year in which a day of year input will be calculated. Only
        applies to day of year input used with the `pyephem` or `nrel`
        methods.

    kwargs :
        Passed to :py:func:`~pvlib.solarposition.nrel_earthsun_distance`.

    Returns
    -------
    dni_extra : float, array, or Series
        The extraterrestrial radiation normal to the sun.
        Pandas Timestamp and DatetimeIndex inputs for ``datetime_or_doy``
        will return ``dni_extra`` as a Pandas TimeSeries. All other input
        data types will yield ``dni_extra`` as a float or an array of floats.
        See :term:`dni_extra`. [Wm⁻²]

    References
    ----------
    .. [1] M. Reno, C. Hansen, and J. Stein, "Global Horizontal Irradiance
       Clear Sky Models: Implementation and Analysis", Sandia National
       Laboratories, SAND2012-2389, 2012.
       :doi:`10.2172/1039404`

    .. [2] J. A. Duffie, W. A. Beckman, N. Blair, "Solar Radiation", in Solar
       Engineering of Thermal Processes, Photovoltaics and Wind, 5th ed,
       New York, USA: J. Wiley and Sons, 2020, pp. 3-44.
       :doi:`10.1002/9781119540328`

    .. [3] J. W. Spencer, "Fourier series representation of the sun," Search,
       vol. 2, p. 172, 1971.

    .. [4] R. G. Allen et al., Eds. The ASCE standardized reference
       evapotranspiration equation. Reston, Va.: American Society of Civil
       Engineers, 2005. :doi:`10.1061/9780784408056`

    .. [6] I. Reda, A. Andreas, "Solar position algorithm for solar
       radiation applications" NREL Golden, USA. NREL/TP-560-34302,
       Revised 2008. :doi:`10.2172/15003974`
    """

    to_doy, to_datetimeindex, to_output = \
        _handle_extra_radiation_types(datetime_or_doy, epoch_year)

    # consider putting asce and spencer methods in their own functions
    method = method.lower()
    if method == 'asce':
        B = solarposition._calculate_simple_day_angle(to_doy(datetime_or_doy),
                                                      offset=0)
        RoverR0sqrd = 1 + 0.033 * np.cos(B)
    elif method == 'spencer':
        B = solarposition._calculate_simple_day_angle(to_doy(datetime_or_doy))
        RoverR0sqrd = (1.00011 + 0.034221 * np.cos(B) + 0.00128 * np.sin(B) +
                       0.000719 * np.cos(2 * B) + 7.7e-05 * np.sin(2 * B))
    elif method == 'pyephem':
        times = to_datetimeindex(datetime_or_doy)
        RoverR0sqrd = solarposition.pyephem_earthsun_distance(times) ** (-2)
    elif method == 'nrel':
        times = to_datetimeindex(datetime_or_doy)
        RoverR0sqrd = \
            solarposition.nrel_earthsun_distance(times, **kwargs) ** (-2)
    else:
        raise ValueError('Invalid method: %s', method)

    Ea = solar_constant * RoverR0sqrd

    Ea = to_output(Ea)

    return Ea


def aoi_projection(surface_tilt, surface_azimuth, solar_zenith, solar_azimuth):
    """
    Calculates the dot product of the sun position unit vector and the surface
    normal unit vector; in other words, the cosine of the angle of incidence.

    Usage note: When the sun is behind the surface the value returned is
    negative.  For many uses negative values must be set to zero.

    Input all angles in degrees.

    Parameters
    ----------
    surface_tilt : numeric
        Panel tilt from horizontal. See :term:`surface_tilt`. [°]

    surface_azimuth : numeric
        Panel azimuth. See :term:`surface_azimuth`. [°]

    solar_zenith : numeric
        Solar zenith angle. See :term:`solar_zenith`. [°]

    solar_azimuth : numeric
        Solar azimuth angle. See :term:`solar_azimuth`. [°]

    Returns
    -------
    projection : numeric
        Dot product of panel normal and solar angle.
        See :term:`aoi_projection`.
    """

    projection = (
        tools.cosd(surface_tilt) * tools.cosd(solar_zenith) +
        tools.sind(surface_tilt) * tools.sind(solar_zenith) *
        tools.cosd(solar_azimuth - surface_azimuth))

    # GH 1185
    projection = np.clip(projection, -1, 1)

    try:
        projection.name = 'aoi_projection'
    except AttributeError:
        pass

    return projection


def aoi(surface_tilt, surface_azimuth, solar_zenith, solar_azimuth):
    """
    Calculates the angle of incidence of the solar vector on a surface.
    This is the angle between the solar vector and the surface normal.

    Input all angles in degrees.

    Parameters
    ----------
    surface_tilt : numeric
        Panel tilt from horizontal. See :term:`surface_tilt`. [°]
    surface_azimuth : numeric
        Panel azimuth. See :term:`surface_azimuth`. [°]
    solar_zenith : numeric
        Solar zenith angle. See :term:`solar_zenith`. [°]
    solar_azimuth : numeric
        Solar azimuth angle. See :term:`solar_azimuth`. [°]

    Returns
    -------
    aoi : numeric
        Angle of incidence, see :term:`aoi`. [°]
    """

    projection = aoi_projection(surface_tilt, surface_azimuth,
                                solar_zenith, solar_azimuth)
    aoi_value = np.rad2deg(np.arccos(projection))

    try:
        aoi_value.name = 'aoi'
    except AttributeError:
        pass

    return aoi_value


def perez(surface_tilt, surface_azimuth, dhi, dni, dni_extra,
          solar_zenith, solar_azimuth, airmass,
          model='allsitescomposite1990', return_components=False):
    '''
    Determine diffuse irradiance from the sky on a tilted surface using
    one of the Perez models.

    Perez models determine the diffuse irradiance from the sky (ground
    reflected irradiance is not included in this algorithm) on a tilted
    surface using the surface tilt angle, surface azimuth angle, diffuse
    horizontal irradiance, direct normal irradiance, extraterrestrial
    irradiance, sun zenith angle, sun azimuth angle, and relative (not
    pressure-corrected) airmass. Optionally a selector may be used to
    use any of Perez's model coefficient sets.

    Warning
    -------
    The Perez transposition model features discontinuities in the
    predicted tilted diffuse irradiance due to relying on discrete input
    values. For applications that benefit from continuous output, consider
    using :py:func:`~pvlib.irradiance.perez_driesse`.

    Parameters
    ----------
    surface_tilt : numeric
        Surface tilt angle. See :term:`surface_tilt`.
        [°]

    surface_azimuth : numeric
        Surface azimuth angle. See :term:`surface_azimuth`. [°]

    dhi : numeric
        Diffuse horizontal irradiance, must be >=0. [Wm⁻²]

    dni : numeric
        Direct normal irradiance, must be >=0. [Wm⁻²]


    dni_extra : numeric
        Extraterrestrial normal irradiance. [Wm⁻²]

    solar_zenith : numeric
        apparent (refraction-corrected) zenith angle. [°]

    solar_azimuth : numeric
        Solar azimuth angle. See :term:`solar_azimuth`. [°]

    airmass : numeric
        Relative (not pressure-corrected) airmass values. If AM is a
        DataFrame it must be of the same size as all other DataFrame
        inputs. AM must be >=0 (careful using the 1/sec(z) model of AM
        generation). [unitless]

    model : string, default 'allsitescomposite1990'
        A string which selects the desired set of Perez coefficients. If
        model is not provided as an input, the default, '1990' will be
        used. All possible model selections are:

        * '1990'
        * 'allsitescomposite1990' (same as '1990')
        * 'allsitescomposite1988'
        * 'sandiacomposite1988'
        * 'usacomposite1988'
        * 'france1988'
        * 'phoenix1988'
        * 'elmonte1988'
        * 'osage1988'
        * 'albuquerque1988'
        * 'capecanaveral1988'
        * 'albany1988'

    return_components : bool, default False
        Flag used to decide whether to return the calculated diffuse components
        or not.

    Returns
    --------
    numeric, OrderedDict, or DataFrame
        Return type controlled by `return_components` argument.
        If ``return_components=False``, `sky_diffuse` is returned.
        If ``return_components=True``, `diffuse_components` is returned.

    sky_diffuse : numeric
        The sky diffuse component of the solar radiation on a tilted
        surface.

    diffuse_components : OrderedDict (array input) or DataFrame (Series input)
        Keys/columns are:
            * poa_sky_diffuse: Total sky diffuse
            * poa_isotropic
            * poa_circumsolar
            * poa_horizon


    References
    ----------
    .. [1] Loutzenhiser P.G. et. al. "Empirical validation of models to
       compute solar irradiance on inclined surfaces for building energy
       simulation" 2007, Solar Energy vol. 81. pp. 254-267

    .. [2] Perez, R., Seals, R., Ineichen, P., Stewart, R., Menicucci, D.,
       1987. A new simplified version of the Perez diffuse irradiance model
       for tilted surfaces. Solar Energy 39(3), 221-232.

    .. [3] Perez, R., Ineichen, P., Seals, R., Michalsky, J., Stewart, R.,
       1990. Modeling daylight availability and irradiance components from
       direct and global irradiance. Solar Energy 44 (5), 271-289.

    .. [4] Perez, R. et. al 1988. "The Development and Verification of the
       Perez Diffuse Radiation Model". SAND88-7030
    '''

    kappa = 1.041  # for solar_zenith in radians
    z = np.radians(solar_zenith)  # convert to radians

    # delta is the sky's "brightness"
    delta = dhi * airmass / dni_extra

    # epsilon is the sky's "clearness"
    with np.errstate(invalid='ignore'):
        eps = ((dhi + dni) / dhi + kappa * (z ** 3)) / (1 + kappa * (z ** 3))

    # numpy indexing below will not work with a Series
    if isinstance(eps, pd.Series):
        eps = eps.values

    # Perez et al define clearness bins according to the following
    # rules. 1 = overcast ... 8 = clear (these names really only make
    # sense for small zenith angles, but...) these values will
    # eventually be used as indicies for coeffecient look ups
    ebin = np.digitize(eps, (0., 1.065, 1.23, 1.5, 1.95, 2.8, 4.5, 6.2))
    ebin = np.array(ebin)  # GH 642
    ebin[np.isnan(eps)] = 0

    # correct for 0 indexing in coeffecient lookup
    # later, ebin = -1 will yield nan coefficients
    ebin -= 1

    # The various possible sets of Perez coefficients are contained
    # in a subfunction to clean up the code.
    F1c, F2c = _get_perez_coefficients(model)

    # results in invalid eps (ebin = -1) being mapped to nans
    nans = np.array([np.nan, np.nan, np.nan])
    F1c = np.vstack((F1c, nans))
    F2c = np.vstack((F2c, nans))

    F1 = (F1c[ebin, 0] + F1c[ebin, 1] * delta + F1c[ebin, 2] * z)
    F1 = np.maximum(F1, 0)

    F2 = (F2c[ebin, 0] + F2c[ebin, 1] * delta + F2c[ebin, 2] * z)

    A = aoi_projection(surface_tilt, surface_azimuth,
                       solar_zenith, solar_azimuth)
    A = np.maximum(A, 0)

    B = tools.cosd(solar_zenith)
    B = np.maximum(B, tools.cosd(85))

    # Calculate Diffuse POA from sky dome
    term1 = 0.5 * (1 - F1) * (1 + tools.cosd(surface_tilt))
    term2 = F1 * A / B
    term3 = F2 * tools.sind(surface_tilt)

    sky_diffuse = np.maximum(dhi * (term1 + term2 + term3), 0)

    # we've preserved the input type until now, so don't ruin it!
    if isinstance(sky_diffuse, pd.Series):
        sky_diffuse[np.isnan(airmass)] = 0
    else:
        sky_diffuse = np.where(np.isnan(airmass), 0, sky_diffuse)

    if return_components:
        diffuse_components = OrderedDict()
        diffuse_components['poa_sky_diffuse'] = sky_diffuse

        # Calculate the different components
        diffuse_components['poa_isotropic'] = dhi * term1
        diffuse_components['poa_circumsolar'] = dhi * term2
        diffuse_components['poa_horizon'] = dhi * term3

        # Set values of components to 0 when sky_diffuse is 0
        mask = sky_diffuse == 0
        if isinstance(sky_diffuse, pd.Series):
            diffuse_components = pd.DataFrame(diffuse_components)
            diffuse_components.loc[mask] = 0
        else:
            diffuse_components = {k: np.where(mask, 0, v) for k, v in
                                  diffuse_components.items()}
        return diffuse_components
    else:
        return sky_diffuse


def _get_perez_coefficients(perezmodel):
    '''
    Find coefficients for the Perez model

    Parameters
    ----------

    perezmodel : string, default 'allsitescomposite1990'

          a character string which selects the desired set of Perez
          coefficients. If model is not provided as an input, the default,
          '1990' will be used.

    All possible model selections are:

          * '1990'
          * 'allsitescomposite1990' (same as '1990')
          * 'allsitescomposite1988'
          * 'sandiacomposite1988'
          * 'usacomposite1988'
          * 'france1988'
          * 'phoenix1988'
          * 'elmonte1988'
          * 'osage1988'
          * 'albuquerque1988'
          * 'capecanaveral1988'
          * 'albany1988'

    Returns
    --------
    F1coeffs, F2coeffs : (array, array)
          F1 and F2 coefficients for the Perez model

    References
    ----------
    .. [1] Loutzenhiser P.G. et. al. "Empirical validation of models to
       compute solar irradiance on inclined surfaces for building energy
       simulation" 2007, Solar Energy vol. 81. pp. 254-267

    .. [2] Perez, R., Seals, R., Ineichen, P., Stewart, R., Menicucci, D.,
       1987. A new simplified version of the Perez diffuse irradiance model
       for tilted surfaces. Solar Energy 39(3), 221-232.

    .. [3] Perez, R., Ineichen, P., Seals, R., Michalsky, J., Stewart, R.,
       1990. Modeling daylight availability and irradiance components from
       direct and global irradiance. Solar Energy 44 (5), 271-289.

    .. [4] Perez, R. et. al 1988. "The Development and Verification of the
       Perez Diffuse Radiation Model". SAND88-7030

    '''
    coeffdict = {
        'allsitescomposite1990': [
            [-0.0080,    0.5880,   -0.0620,   -0.0600,    0.0720,   -0.0220],
            [0.1300,    0.6830,   -0.1510,   -0.0190,    0.0660,   -0.0290],
            [0.3300,    0.4870,   -0.2210,    0.0550,   -0.0640,   -0.0260],
            [0.5680,    0.1870,   -0.2950,    0.1090,   -0.1520,   -0.0140],
            [0.8730,   -0.3920,   -0.3620,    0.2260,   -0.4620,    0.0010],
            [1.1320,   -1.2370,   -0.4120,    0.2880,   -0.8230,    0.0560],
            [1.0600,   -1.6000,   -0.3590,    0.2640,   -1.1270,    0.1310],
            [0.6780,   -0.3270,   -0.2500,    0.1560,   -1.3770,    0.2510]],
        'allsitescomposite1988': [
            [-0.0180,    0.7050,   -0.071,   -0.0580,    0.1020,   -0.0260],
            [0.1910,    0.6450,   -0.1710,    0.0120,    0.0090,   -0.0270],
            [0.4400,    0.3780,   -0.2560,    0.0870,   -0.1040,   -0.0250],
            [0.7560,   -0.1210,   -0.3460,    0.1790,   -0.3210,   -0.0080],
            [0.9960,   -0.6450,   -0.4050,    0.2600,   -0.5900,    0.0170],
            [1.0980,   -1.2900,   -0.3930,    0.2690,   -0.8320,    0.0750],
            [0.9730,   -1.1350,   -0.3780,    0.1240,   -0.2580,    0.1490],
            [0.6890,   -0.4120,   -0.2730,    0.1990,   -1.6750,    0.2370]],
        'sandiacomposite1988': [
            [-0.1960,    1.0840,   -0.0060,   -0.1140,    0.1800,   -0.0190],
            [0.2360,    0.5190,   -0.1800,   -0.0110,    0.0200,   -0.0380],
            [0.4540,    0.3210,   -0.2550,    0.0720,   -0.0980,   -0.0460],
            [0.8660,   -0.3810,   -0.3750,    0.2030,   -0.4030,   -0.0490],
            [1.0260,   -0.7110,   -0.4260,    0.2730,   -0.6020,   -0.0610],
            [0.9780,   -0.9860,   -0.3500,    0.2800,   -0.9150,   -0.0240],
            [0.7480,   -0.9130,   -0.2360,    0.1730,   -1.0450,    0.0650],
            [0.3180,   -0.7570,    0.1030,    0.0620,   -1.6980,    0.2360]],
        'usacomposite1988': [
            [-0.0340,    0.6710,   -0.0590,   -0.0590,    0.0860,   -0.0280],
            [0.2550,    0.4740,   -0.1910,    0.0180,   -0.0140,   -0.0330],
            [0.4270,    0.3490,   -0.2450,    0.0930,   -0.1210,   -0.0390],
            [0.7560,   -0.2130,   -0.3280,    0.1750,   -0.3040,   -0.0270],
            [1.0200,   -0.8570,   -0.3850,    0.2800,   -0.6380,   -0.0190],
            [1.0500,   -1.3440,   -0.3480,    0.2800,   -0.8930,    0.0370],
            [0.9740,   -1.5070,   -0.3700,    0.1540,   -0.5680,    0.1090],
            [0.7440,   -1.8170,   -0.2560,    0.2460,   -2.6180,    0.2300]],
        'france1988': [
            [0.0130,    0.7640,   -0.1000,   -0.0580,    0.1270,   -0.0230],
            [0.0950,    0.9200,   -0.1520,         0,    0.0510,   -0.0200],
            [0.4640,    0.4210,   -0.2800,    0.0640,   -0.0510,   -0.0020],
            [0.7590,   -0.0090,   -0.3730,    0.2010,   -0.3820,    0.0100],
            [0.9760,   -0.4000,   -0.4360,    0.2710,   -0.6380,    0.0510],
            [1.1760,   -1.2540,   -0.4620,    0.2950,   -0.9750,    0.1290],
            [1.1060,   -1.5630,   -0.3980,    0.3010,   -1.4420,    0.2120],
            [0.9340,   -1.5010,   -0.2710,    0.4200,   -2.9170,    0.2490]],
        'phoenix1988': [
            [-0.0030,    0.7280,   -0.0970,   -0.0750,    0.1420,   -0.0430],
            [0.2790,    0.3540,   -0.1760,    0.0300,   -0.0550,   -0.0540],
            [0.4690,    0.1680,   -0.2460,    0.0480,   -0.0420,   -0.0570],
            [0.8560,   -0.5190,   -0.3400,    0.1760,   -0.3800,   -0.0310],
            [0.9410,   -0.6250,   -0.3910,    0.1880,   -0.3600,   -0.0490],
            [1.0560,   -1.1340,   -0.4100,    0.2810,   -0.7940,   -0.0650],
            [0.9010,   -2.1390,   -0.2690,    0.1180,   -0.6650,    0.0460],
            [0.1070,    0.4810,    0.1430,   -0.1110,   -0.1370,    0.2340]],
        'elmonte1988': [
            [0.0270,    0.7010,   -0.1190,   -0.0580,    0.1070,  -0.0600],
            [0.1810,    0.6710,   -0.1780,   -0.0790,    0.1940,  -0.0350],
            [0.4760,    0.4070,   -0.2880,    0.0540,   -0.0320,  -0.0550],
            [0.8750,   -0.2180,   -0.4030,    0.1870,   -0.3090,  -0.0610],
            [1.1660,   -1.0140,   -0.4540,    0.2110,   -0.4100,  -0.0440],
            [1.1430,   -2.0640,   -0.2910,    0.0970,   -0.3190,   0.0530],
            [1.0940,   -2.6320,   -0.2590,    0.0290,   -0.4220,   0.1470],
            [0.1550,    1.7230,    0.1630,   -0.1310,   -0.0190,   0.2770]],
        'osage1988': [
            [-0.3530,    1.4740,   0.0570,   -0.1750,    0.3120,   0.0090],
            [0.3630,    0.2180,  -0.2120,    0.0190,   -0.0340,  -0.0590],
            [-0.0310,    1.2620,  -0.0840,   -0.0820,    0.2310,  -0.0170],
            [0.6910,    0.0390,  -0.2950,    0.0910,   -0.1310,  -0.0350],
            [1.1820,   -1.3500,  -0.3210,    0.4080,   -0.9850,  -0.0880],
            [0.7640,    0.0190,  -0.2030,    0.2170,   -0.2940,  -0.1030],
            [0.2190,    1.4120,   0.2440,    0.4710,   -2.9880,   0.0340],
            [3.5780,   22.2310, -10.7450,    2.4260,    4.8920,  -5.6870]],
        'albuquerque1988': [
            [0.0340,    0.5010,  -0.0940,   -0.0630,    0.1060,  -0.0440],
            [0.2290,    0.4670,  -0.1560,   -0.0050,   -0.0190,  -0.0230],
            [0.4860,    0.2410,  -0.2530,    0.0530,   -0.0640,  -0.0220],
            [0.8740,   -0.3930,  -0.3970,    0.1810,   -0.3270,  -0.0370],
            [1.1930,   -1.2960,  -0.5010,    0.2810,   -0.6560,  -0.0450],
            [1.0560,   -1.7580,  -0.3740,    0.2260,   -0.7590,   0.0340],
            [0.9010,   -4.7830,  -0.1090,    0.0630,   -0.9700,   0.1960],
            [0.8510,   -7.0550,  -0.0530,    0.0600,   -2.8330,   0.3300]],
        'capecanaveral1988': [
            [0.0750,    0.5330,   -0.1240,  -0.0670,   0.0420,  -0.0200],
            [0.2950,    0.4970,   -0.2180,  -0.0080,   0.0030,  -0.0290],
            [0.5140,    0.0810,   -0.2610,   0.0750,  -0.1600,  -0.0290],
            [0.7470,   -0.3290,   -0.3250,   0.1810,  -0.4160,  -0.0300],
            [0.9010,   -0.8830,   -0.2970,   0.1780,  -0.4890,   0.0080],
            [0.5910,   -0.0440,   -0.1160,   0.2350,  -0.9990,   0.0980],
            [0.5370,   -2.4020,    0.3200,   0.1690,  -1.9710,   0.3100],
            [-0.8050,    4.5460,    1.0720,  -0.2580,  -0.9500,    0.7530]],
        'albany1988': [
            [0.0120,    0.5540,   -0.0760, -0.0520,   0.0840,  -0.0290],
            [0.2670,    0.4370,   -0.1940,  0.0160,   0.0220,  -0.0360],
            [0.4200,    0.3360,   -0.2370,  0.0740,  -0.0520,  -0.0320],
            [0.6380,   -0.0010,   -0.2810,  0.1380,  -0.1890,  -0.0120],
            [1.0190,   -1.0270,   -0.3420,  0.2710,  -0.6280,   0.0140],
            [1.1490,   -1.9400,   -0.3310,  0.3220,  -1.0970,   0.0800],
            [1.4340,   -3.9940,   -0.4920,  0.4530,  -2.3760,   0.1170],
            [1.0070,   -2.2920,   -0.4820,  0.3900,  -3.3680,   0.2290]], }

    array = np.array(coeffdict[perezmodel])

    F1coeffs = array[:, 0:3]
    F2coeffs = array[:, 3:7]

    return F1coeffs, F2coeffs


def get_total_irradiance(surface_tilt, surface_azimuth,
                         solar_zenith, solar_azimuth,
                         dni, ghi, dhi, dni_extra=None, airmass=None,
                         albedo=0.25, surface_type=None,
                         model='isotropic',
                         model_perez='allsitescomposite1990'):
    r"""
    Determine total in-plane irradiance and its beam, sky diffuse and ground
    reflected components, using the specified sky diffuse irradiance model.

    .. math::

       I_{tot} = I_{beam} + I_{sky diffuse} + I_{ground}

    Sky diffuse models include:
        * isotropic (default)
        * klucher
        * haydavies
        * reindl
        * king
        * perez
        * perez-driesse

    Parameters
    ----------
    surface_tilt : numeric
        Panel tilt from horizontal. See :term:`surface_tilt`. [°]
    surface_azimuth : numeric
        Panel azimuth. See :term:`surface_azimuth`. [°]
    solar_zenith : numeric
        Solar zenith angle. See :term:`solar_zenith`. [°]
    solar_azimuth : numeric
        Solar azimuth angle. See :term:`solar_azimuth`. [°]
    dni : numeric
        Direct normal irradiance. See :term:`dni`. [Wm⁻²]
    ghi : numeric
        Global horizontal irradiance. See :term:`ghi`. [Wm⁻²]
    dhi : numeric
        Diffuse horizontal irradiance. See :term:`dhi`. [Wm⁻²]
    dni_extra : numeric, optional
        Extraterrestrial direct normal irradiance. See :term:`dni_extra`.
        [Wm⁻²]
    airmass : numeric, optional
        Relative airmass, not adjusted for pressure.
        See :term:`airmass_relative`. [unitless]
    albedo : numeric, default 0.25
        Ground surface albedo. See :term:`albedo`. [unitless]
    surface_type : str, optional
        Surface type. See :py:func:`~pvlib.irradiance.get_ground_diffuse` for
        the list of accepted values.
    model : str, default 'isotropic'
        Irradiance model. Can be one of ``'isotropic'``, ``'klucher'``,
        ``'haydavies'``, ``'reindl'``, ``'king'``, ``'perez'``,
        ``'perez-driesse'``.
    model_perez : str, default 'allsitescomposite1990'
        Used only if ``model='perez'``. See :py:func:`~pvlib.irradiance.perez`.

    Returns
    -------
    total_irrad : OrderedDict or DataFrame
        Contains keys/columns ``'poa_global', 'poa_direct', 'poa_diffuse',
        'poa_sky_diffuse', 'poa_ground_diffuse'``. [Wm⁻²]

    Notes
    -----
    Models ``'haydavies'``, ``'reindl'``, ``'perez'`` and ``'perez-driesse'``
    require ``'dni_extra'``. Values can be calculated using
    :py:func:`~pvlib.irradiance.get_extra_radiation`.

    The ``'perez'`` and ``'perez-driesse'`` models require relative airmass
    (``airmass``) as input. If ``airmass`` is not provided, it is calculated
    using the defaults in :py:func:`~pvlib.atmosphere.get_relative_airmass`.
    """

    poa_sky_diffuse = get_sky_diffuse(
        surface_tilt, surface_azimuth, solar_zenith, solar_azimuth,
        dni, ghi, dhi, dni_extra=dni_extra, airmass=airmass, model=model,
        model_perez=model_perez)

    poa_ground_diffuse = get_ground_diffuse(surface_tilt, ghi, albedo,
                                            surface_type)
    aoi_ = aoi(surface_tilt, surface_azimuth, solar_zenith, solar_azimuth)
    irrads = poa_components(aoi_, dni, poa_sky_diffuse, poa_ground_diffuse)
    return irrads


def get_sky_diffuse(surface_tilt, surface_azimuth,
                    solar_zenith, solar_azimuth,
                    dni, ghi, dhi, dni_extra=None, airmass=None,
                    model='isotropic',
                    model_perez='allsitescomposite1990'):
    r"""
    Determine in-plane sky diffuse irradiance component
    using the specified sky diffuse irradiance model.

    Sky diffuse models include:
        * isotropic (default)
        * klucher
        * haydavies
        * reindl
        * king
        * perez
        * perez-driesse

    Parameters
    ----------
    surface_tilt : numeric
        Panel tilt from horizontal. See :term:`surface_tilt`. [°]
    surface_azimuth : numeric
        Panel azimuth. See :term:`surface_azimuth`. [°]
    solar_zenith : numeric
        Solar zenith angle. See :term:`solar_zenith`. [°]
    solar_azimuth : numeric
        Solar azimuth angle. See :term:`solar_azimuth`. [°]
    dni : numeric
        Direct normal irradiance. See :term:`dni`. [Wm⁻²]
    ghi : numeric
        Global horizontal irradiance. See :term:`ghi`. [Wm⁻²]
    dhi : numeric
        Diffuse horizontal irradiance. See :term:`dhi`. [Wm⁻²]
    dni_extra : numeric, optional
        Extraterrestrial direct normal irradiance. See :term:`dni_extra`.
        [Wm⁻²]
    airmass : numeric, optional
        Relative airmass, not adjusted for pressure.
        See :term:`airmass_relative`. [unitless]
    model : str, default 'isotropic'
        Irradiance model. Can be one of ``'isotropic'``, ``'klucher'``,
        ``'haydavies'``, ``'reindl'``, ``'king'``, ``'perez'``,
        ``'perez-driesse'``.
    model_perez : str, default 'allsitescomposite1990'
        Used only if ``model='perez'``. See :py:func:`~pvlib.irradiance.perez`.

    Returns
    -------
    poa_sky_diffuse : numeric
        Sky diffuse irradiance in the plane of array. [Wm⁻²]

    Raises
    ------
    ValueError
        If model is one of ``'haydavies'``, ``'reindl'``, ``'perez'``,  or
        ``'perez_driesse'`` and ``dni_extra`` is not specified.

    Notes
    -----
    Models ``'haydavies'``, ``'reindl'``, ``'perez'`` and ``'perez-driesse'``
    require ``'dni_extra'``. Values can be calculated using
    :py:func:`~pvlib.irradiance.get_extra_radiation`.

    The ``'Perez'`` transposition model features discontinuities in the
    predicted tilted diffuse irradiance due to relying on discrete input
    values. For applications that benefit from continuous output, consider
    using :py:func:`~pvlib.irradiance.perez_driesse`.

    The ``'perez'`` and ``'perez-driesse'`` models require relative airmass
    (``airmass``) as input. If ``airmass`` is not provided, it is calculated
    using the defaults in :py:func:`~pvlib.atmosphere.get_relative_airmass`.
    """

    model = model.lower()

    if dni_extra is None and model in {'haydavies', 'reindl',
                                       'perez', 'perez-driesse'}:
        raise ValueError(f'dni_extra is required for model {model}')

    if model == 'isotropic':
        sky = isotropic(surface_tilt, dhi)
    elif model == 'klucher':
        sky = klucher(surface_tilt, surface_azimuth, dhi, ghi,
                      solar_zenith, solar_azimuth)
    elif model == 'haydavies':
        sky = haydavies(surface_tilt, surface_azimuth, dhi, dni, dni_extra,
                        solar_zenith, solar_azimuth)
    elif model == 'reindl':
        sky = reindl(surface_tilt, surface_azimuth, dhi, dni, ghi, dni_extra,
                     solar_zenith, solar_azimuth)
    elif model == 'king':
        sky = king(surface_tilt, dhi, ghi, solar_zenith)
    elif model == 'perez':
        if airmass is None:
            airmass = atmosphere.get_relative_airmass(solar_zenith)
        sky = perez(surface_tilt, surface_azimuth, dhi, dni, dni_extra,
                    solar_zenith, solar_azimuth, airmass,
                    model=model_perez)
    elif model == 'perez-driesse':
        # perez_driesse will calculate its own airmass if needed
        sky = perez_driesse(surface_tilt, surface_azimuth, dhi, dni, dni_extra,
                            solar_zenith, solar_azimuth, airmass)
    else:
        raise ValueError(f'invalid model selection {model}')

    return sky


def isotropic(surface_tilt, dhi):
    r'''
    Determine diffuse irradiance from the sky on a tilted surface using
    the isotropic sky model.

    .. math::

       I_{d} = DHI \frac{1 + \cos\beta}{2}

    Hottel and Woertz's model treats the sky as a uniform source of
    diffuse irradiance. Thus, the diffuse irradiance from the sky (ground
    reflected irradiance is not included in this algorithm) on a tilted
    surface can be found from the diffuse horizontal irradiance and the
    tilt angle of the surface. A discussion of the origin of the
    isotropic model can be found in [2]_.

    Parameters
    ----------
    surface_tilt : numeric
        Panel tilt from horizontal. See :term:`surface_tilt`. [°]

    dhi : numeric
        Diffuse horizontal irradiance, must be >=0. See :term:`dhi`.

    Returns
    -------
    diffuse : numeric
        The sky diffuse component of the solar radiation. [Wm⁻²]

    References
    ----------
    .. [1] Loutzenhiser P.G. et al. "Empirical validation of models to
       compute solar irradiance on inclined surfaces for building energy
       simulation" 2007, Solar Energy vol. 81. pp. 254-267
       :doi:`10.1016/j.solener.2006.03.009`

    .. [2] Kamphuis, N.R. et al. "Perspectives on the origin, derivation,
       meaning, and significance of the isotropic sky model" 2020, Solar
       Energy vol. 201. pp. 8-12
       :doi:`10.1016/j.solener.2020.02.067`
    '''
    sky_diffuse = dhi * (1 + tools.cosd(surface_tilt)) * 0.5

    return sky_diffuse


def get_ground_diffuse(surface_tilt, ghi, albedo=.25, surface_type=None):
    r'''
    Estimate diffuse irradiance on a tilted surface from ground reflections.

    Ground diffuse irradiance is calculated as

    .. math::

       G_{ground} = GHI \times \rho \times \frac{1 - \cos\beta}{2}

    where :math:`\rho` is ``albedo`` and :math:`\beta` is ``surface_tilt``.

    Parameters
    ----------
    surface_tilt : numeric
        Panel tilt from horizontal. See :term:`surface_tilt`. [°]

    ghi : numeric
        Global horizontal irradiance. See :term:`ghi`. [Wm⁻²]

    albedo : numeric, default 0.25
        Ground surface albedo., typically 0.1-0.4 for bare or vegetated ground,
        may increase over snow, ice, etc. May also be known as
        the reflection coefficient. Must be >=0 and <=1. Will be
        overridden if ``surface_type`` is supplied. See :term:`albedo`.
        [unitless]

    surface_type : string, optional
        If supplied, overrides ``albedo``. ``surface_type`` can be one of
        'urban', 'grass', 'fresh grass', 'snow', 'fresh snow', 'asphalt',
        'concrete', 'aluminum', 'copper', 'fresh steel', 'dirty steel',
        'sea'.

    Returns
    -------
    grounddiffuse : numeric
        Ground reflected irradiance. [Wm⁻²]

    Notes
    -----
    Table of albedo values by ``surface_type`` are from [2]_, [3]_, [4]_;
    see :py:const:`~pvlib.albedo.SURFACE_ALBEDOS`.

    References
    ----------
    .. [1] Loutzenhiser P.G. et. al. "Empirical validation of models to compute
       solar irradiance on inclined surfaces for building energy simulation"
       2007, Solar Energy vol. 81. pp. 254-267.
    .. [2] https://www.pvsyst.com/help/albedo.htm Accessed January, 2024.
    .. [3] http://en.wikipedia.org/wiki/Albedo Accessed January, 2024.
    .. [4] Payne, R. E. "Albedo of the Sea Surface". J. Atmos. Sci., 29,
       pp. 959–970, 1972.
       :doi:`10.1175/1520-0469(1972)029<0959:AOTSS>2.0.CO;2`
    '''

    if surface_type is not None:
        albedo = pvlib.albedo.SURFACE_ALBEDOS[surface_type]

    diffuse_irrad = ghi * albedo * (1 - np.cos(np.radians(surface_tilt))) * 0.5

    try:
        diffuse_irrad.name = 'diffuse_ground'
    except AttributeError:
        pass

    return diffuse_irrad


def poa_components(aoi, dni, poa_sky_diffuse, poa_ground_diffuse):
    r'''
    Determine in-plane irradiance components.

    Combines DNI with sky diffuse and ground-reflected irradiance to calculate
    total, direct and diffuse irradiance components in the plane of array.

    Parameters
    ----------
    aoi : numeric
        Angle of incidence of solar rays with respect to the module
        surface. See :term:`aoi`. [°]

    dni : numeric
        Direct normal irradiance, as measured from a TMY file or
        calculated with a clearsky model. See :term:`dni`. [Wm⁻²]

    poa_sky_diffuse : numeric
        Diffuse irradiance in the plane of the modules, as
        calculated by a diffuse irradiance translation function. [Wm⁻²]

    poa_ground_diffuse : numeric
        Ground-reflected irradiance in the plane of the modules,
        as calculated by an albedo model (eg. :func:`grounddiffuse`). [Wm⁻²]

    Returns
    -------
    irrads : OrderedDict or DataFrame
        Contains the following keys:

        * ``poa_global`` : Total in-plane irradiance. [Wm⁻²]
        * ``poa_direct`` : Total in-plane beam irradiance. [Wm⁻²]
        * ``poa_diffuse`` : Total in-plane diffuse irradiance. [Wm⁻²]
        * ``poa_sky_diffuse`` : In-plane diffuse irradiance from sky. [Wm⁻²]
        * ``poa_ground_diffuse`` : In-plane diffuse irradiance from ground.
          [Wm⁻²]

    Notes
    ------
    Negative beam irradiation due to AOI > 90° or AOI < 0° is set to zero.
    '''

    poa_direct = np.maximum(dni * np.cos(np.radians(aoi)), 0)
    poa_diffuse = poa_sky_diffuse + poa_ground_diffuse
    poa_global = poa_direct + poa_diffuse

    irrads = OrderedDict()
    irrads['poa_global'] = poa_global
    irrads['poa_direct'] = poa_direct
    irrads['poa_diffuse'] = poa_diffuse
    irrads['poa_sky_diffuse'] = poa_sky_diffuse
    irrads['poa_ground_diffuse'] = poa_ground_diffuse

    if isinstance(poa_direct, pd.Series):
        irrads = pd.DataFrame(irrads)

    return irrads


def get_relative_airmass(zenith, model='kastenyoung1989'):
    '''
    Calculate relative (not pressure-adjusted) airmass at sea level.

    Parameter ``model`` allows selection of different airmass models.

    Parameters
    ----------
    zenith : numeric
        Zenith angle of the sun. [degrees]

    model : string, default 'kastenyoung1989'
        Available models include the following:

        * 'simple' - secant(apparent zenith angle) -
          Note that this gives -Inf at zenith=90
        * 'kasten1966' - See [1]_ - requires apparent sun zenith
        * 'youngirvine1967' - See [2]_ - requires true sun zenith
        * 'kastenyoung1989' (default) - See [3]_ - requires apparent sun zenith
        * 'gueymard1993' - See [4]_, [5]_ - requires apparent sun zenith
        * 'young1994' - See [6]_ - requires true sun zenith
        * 'pickering2002' - See [7]_ - requires apparent sun zenith
        * 'gueymard2003' - See [8]_, [9]_ - requires apparent sun zenith

    Returns
    -------
    airmass_relative : numeric
        Relative airmass at sea level. Returns NaN values for any
        zenith angle greater than 90 degrees. [unitless]

    Notes
    -----
    Some models use apparent (refraction-adjusted) zenith angle while
    other models use true (not refraction-adjusted) zenith angle. Apparent
    zenith angles should be calculated at sea level.

    Comparison among several models is reported in [10]_.

    References
    ----------
    .. [1] Fritz Kasten, "A New Table and Approximation Formula for the
       Relative Optical Air Mass," CRREL (U.S. Army), Hanover, NH, USA,
       Technical Report 136, 1965.
       :doi:`11681/5671`

    .. [2] A. T. Young and W. M. Irvine, "Multicolor Photoelectric
       Photometry of the Brighter Planets. I. Program and Procedure,"
       The Astronomical Journal, vol. 72, pp. 945-950, 1967.
       :doi:`10.1086/110366`

    .. [3] Fritz Kasten and Andrew Young, "Revised optical air mass tables
       and approximation formula," Applied Optics 28:4735-4738, 1989.
       :doi:`10.1364/AO.28.004735`

    .. [4] C. Gueymard, "Critical analysis and performance assessment of
       clear sky solar irradiance models using theoretical and measured
       data," Solar Energy, vol. 51, pp. 121-138, 1993.
       :doi:`10.1016/0038-092X(93)90074-X`

    .. [5] C. Gueymard, "Development and performance assessment of a clear
       sky spectral radiation model,” in Proc. of the 22nd ASES Conference,
       Solar ’93, 1993, pp. 433–438.

    .. [6] A. T. Young, "Air-Mass and Refraction," Applied Optics, vol. 33,
       pp. 1108-1110, Feb. 1994.
       :doi:`10.1364/AO.33.001108`

    .. [7] Keith A. Pickering, "The Southern Limits of the Ancient Star Catalog
       and the Commentary of Hipparchos," DIO, vol. 12, pp. 3-27, Sept. 2002.
       Available at `DIO <http://dioi.org/jc01.pdf>`_

    .. [8] C. Gueymard, "Direct solar transmittance and irradiance
       predictions with broadband models. Part I: detailed theoretical
       performance assessment". Solar Energy, vol 74, pp. 355-379, 2003.
       :doi:`10.1016/S0038-092X(03)00195-6`

    .. [9] C. Gueymard, "Clear-Sky Radiation Models and Aerosol Effects", in
       Solar Resources Mapping: Fundamentals and Applications,
       Polo, J., Martín-Pomares, L., Sanfilippo, A. (Eds), Cham, CH: Springer,
       2019, pp. 137-182.
       :doi:`10.1007/978-3-319-97484-2_5`

    .. [10] Matthew J. Reno, Clifford W. Hansen and Joshua S. Stein, "Global
       Horizontal Irradiance Clear Sky Models: Implementation and Analysis"
       Sandia National Laboratories, Albuquerque, NM, USA, SAND2012-2389, 2012.
       :doi:`10.2172/1039404`

    '''

    # set zenith values greater than 90 to nans
    z = np.where(zenith > 90, np.nan, zenith)
    zenith_rad = np.radians(z)

    model = model.lower()

    if 'kastenyoung1989' == model:
        am = (1.0 / (np.cos(zenith_rad) +
              0.50572*((6.07995 + (90 - z)) ** - 1.6364)))
    elif 'kasten1966' == model:
        am = 1.0 / (np.cos(zenith_rad) + 0.15*((93.885 - z) ** - 1.253))
    elif 'simple' == model:
        am = 1.0 / np.cos(zenith_rad)
    elif 'pickering2002' == model:
        am = (1.0 / (np.sin(np.radians(90 - z +
              244.0 / (165 + 47.0 * (90 - z) ** 1.1)))))
    elif 'youngirvine1967' == model:
        sec_zen = 1.0 / np.cos(zenith_rad)
        am = sec_zen * (1 - 0.0012 * (sec_zen * sec_zen - 1))
    elif 'young1994' == model:
        am = ((1.002432*((np.cos(zenith_rad)) ** 2) +
              0.148386*(np.cos(zenith_rad)) + 0.0096467) /
              (np.cos(zenith_rad) ** 3 +
              0.149864*(np.cos(zenith_rad) ** 2) +
              0.0102963*(np.cos(zenith_rad)) + 0.000303978))
    elif 'gueymard1993' == model:  # [4], Eq. 22 and [5], Eq. 3b
        am = (1.0 / (np.cos(zenith_rad) +
              0.00176759*(z)*((94.37515 - z) ** - 1.21563)))
    elif 'gueymard2003' == model:
        am = (1.0 / (np.cos(zenith_rad) +
              0.48353*(z**0.095846)/(96.741 - z)**1.754))
    else:
        raise ValueError('%s is not a valid model for relativeairmass', model)

    if isinstance(zenith, pd.Series):
        am = pd.Series(am, index=zenith.index)

    return am


def sapm(aoi, module, upper=None):
    r"""
    Determine the incidence angle modifier (IAM) using the SAPM model.

    Parameters
    ----------
    aoi : numeric
        Angle of incidence in degrees. Negative input angles will return
        zeros.

    module : dict-like
        A dict or Series with the SAPM IAM model parameters.
        See the :py:func:`sapm` notes section for more details.

    upper : float, optional
        Upper limit on the results.

    Returns
    -------
    iam : numeric
        The SAPM angle of incidence loss coefficient, termed F2 in [1]_.

    Notes
    -----
    The SAPM [1]_ traditionally does not define an upper limit on the AOI
    loss function and values slightly exceeding 1 may exist for moderate
    angles of incidence (15-40 degrees). However, users may consider
    imposing an upper limit of 1.

    References
    ----------
    .. [1] King, D. et al, 2004, "Sandia Photovoltaic Array Performance
       Model", SAND Report 3535, Sandia National Laboratories, Albuquerque,
       NM.

    .. [2] B.H. King et al, "Procedure to Determine Coefficients for the
       Sandia Array Performance Model (SAPM)," SAND2016-5284, Sandia
       National Laboratories (2016).

    .. [3] B.H. King et al, "Recent Advancements in Outdoor Measurement
       Techniques for Angle of Incidence Effects," 42nd IEEE PVSC (2015).
       :doi:`10.1109/PVSC.2015.7355849`

    See Also
    --------
    pvlib.iam.physical
    pvlib.iam.ashrae
    pvlib.iam.martin_ruiz
    pvlib.iam.interp
    """

    aoi_coeff = [module['B5'], module['B4'], module['B3'], module['B2'],
                 module['B1'], module['B0']]

    iam = np.polyval(aoi_coeff, aoi)
    iam = np.clip(iam, 0, upper)
    # nan tolerant masking
    aoi_lt_0 = np.full_like(aoi, False, dtype='bool')
    np.less(aoi, 0, where=~np.isnan(aoi), out=aoi_lt_0)
    iam = np.where(aoi_lt_0, 0, iam)

    if isinstance(aoi, pd.Series):
        iam = pd.Series(iam, aoi.index)

    return iam


def _calculate_simple_day_angle(dayofyear, offset=1):
    """
    Calculates the day angle for the Earth's orbit around the Sun.

    Parameters
    ----------
    dayofyear : numeric
    offset : int, default 1
        For the Spencer method, offset=1; for the ASCE method, offset=0

    Returns
    -------
    day_angle : numeric
    """
    return (2. * np.pi / 365.) * (dayofyear - offset)
