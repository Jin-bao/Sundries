# extract part of the specified data in the .hdf5 file.

# convert UTC time to GPS time
def UTCToGPS(UTCtime:str) -> float:
  # datetime is a system package
  from datetime import datetime

  # difference between UNIX time and GPS time
  UNIX_GPS_DIFF = 315935983

  if '.' in UTCtime:
    UTCtimeList = UTCtime.split('.')
    GPStime = datetime.strptime(UTCtimeList[0], '%Y-%m-%d %H:%M:%S').timestamp() \
      - UNIX_GPS_DIFF
    GPStime += float('0.' + UTCtimeList[1])
  else:
    GPStime = datetime.strptime(UTCtime, '%Y-%m-%d %H:%M:%S').timestamp() \
      - UNIX_GPS_DIFF

  # eg: UTCToGPS('2015-9-14 9:50:45.4') -> 1126259462.4
  return GPStime

# extract data
def extractData(fileName:str, startTime:str, endTime:str) -> iter:
  # try to import h5py package
  try:
    import h5py
  except:
    raise ModuleNotFoundError("No module named 'h5py'")
  
  # open the .hdf5 file
  fileData = h5py.File(fileName, 'r')

  GPSstart = fileData['meta']['GPSstart'][()]
  timeSpacing = fileData['strain']['Strain'].attrs['Xspacing']
  startTime = UTCToGPS(startTime)
  endTime   = UTCToGPS(endTime)

  from math import ceil, floor
  # data range from start to end
  start = ceil((startTime-GPSstart)/timeSpacing)
  end  = floor((endTime-GPSstart) / timeSpacing)

  # Strain = fileData['strain']['Strain'][()]
  # if end > len(Strain):
  #   # if time out of range
  #   raise IndexError('time out of range')
  # else:
  #   strainPartData = Strain[start:end]
  strainPartData = fileData['strain']['Strain'][start:end]

  # close .hdf5 file and return the extracted data
  fileData.close()
  return strainPartData

if __name__ == '__main__':
  strainPartData = extractData('H-H1_LOSC_4_V1-1126256640-4096.hdf5', \
    '2015-9-14 9:50:45.25', '2015-9-14  9:50:45.5')
  print(strainPartData)
  print(len(strainPartData))