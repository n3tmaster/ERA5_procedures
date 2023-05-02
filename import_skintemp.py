from dolibs import skintemp as st
from datetime import datetime
from datetime import date
import calendar
import pathlib
import urllib.parse
from dateutil.relativedelta import relativedelta

previous_date = date.today() + relativedelta(days=-60)



currentMonth = datetime.now().month
currentYear = datetime.now().year



prevYear = previous_date.year
prevMonth = previous_date.month
prevDay = 1

icount = False
i_month = prevMonth
i_year = prevYear

print('clean old images')

st.del_image('postgresql://satserv:ss!2017pwd@droughtsdi.fi.ibimet.cnr.it/gisdb',
    str(date(prevYear,prevMonth,prevDay)),
    str(date(currentYear,currentMonth,calendar.monthrange(currentYear, currentMonth)[1])))

list_of_days = list(filter(lambda x: isinstance(x,str),['01','02','03','04','05','06','07','08','09','10',
                                '11','12','13','14','15','16','17','18','19','20',
                                '21','22','23','24','25','26','27','28','29','30','31']))

while (icount == False):
    print('Begin procedure for '+str(i_year)+'-'+str(i_month))
    
    st.get_n_save(i_year,i_month,str(pathlib.Path(__file__).parent.resolve()), list_of_days)

    if((i_month == currentMonth) and (i_year == currentYear)):
        icount = True
    else:
        if(i_month == 12):
            i_month = 1
            i_year = i_year + 1
        else:
            i_month = i_month + 1

    

print('done')








