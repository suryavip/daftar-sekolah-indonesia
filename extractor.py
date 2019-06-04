import requests
import json
import mysql.connector

# mengumpulkan areaIDs (kode_wilayah) dari http://jendela.data.kemdikbud.go.id/api/index.php/cwilayah/wilayahKabGet

r = requests.get('http://jendela.data.kemdikbud.go.id/api/index.php/cwilayah/wilayahKabGet')
if r.status_code != 200:
    raise Exception('Gagal mengumpulkan kode_wilayah ({})'.format(r.status_code))

areas = r.json()['data']

areaIDs = [area['kode_wilayah'].strip() for area in areas]
# https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
# print(areaIDs)

# mengumpulkan detail sekolah dari http://jendela.data.kemdikbud.go.id/api/index.php/Csekolah/detailSekolahGET?mst_kode_wilayah=XXXXXX

db = mysql.connector.connect(
    user='root',
    password='',
    database='daftar-sekolah'
)
cursor = db.cursor()

done = 0
for areaID in areaIDs:
    r = requests.get('http://jendela.data.kemdikbud.go.id/api/index.php/Csekolah/detailSekolahGET?mst_kode_wilayah={}'.format(areaID))
    if r.status_code != 200:
        raise Exception('Gagal mengumpulkan data sekolah untuk kode_wilayah {} ({})'.format(areaID, r.status_code))

    schools = r.json()['data']
    columns = schools[0].keys()

    if done == 0:
        # buat table
        cols = ['{} VARCHAR(255) NOT NULL'.format(c) for c in columns]
        cols = ','.join(cols)
        query = 'CREATE TABLE IF NOT EXISTS sekolah ({})'.format(cols)
        cursor.execute((query))

    cols = ','.join(columns)

    val = []
    q = []
    for s in schools:
        val += [s[d] for d in s]
        tq = ['%s' for d in s]
        q.append('({})'.format(','.join(tq)))
    q = ','.join(q)

    query = 'INSERT INTO sekolah ({}) VALUES {}'.format(cols, q)
    cursor.execute((query), tuple(val))

    '''result = {}
    result[areaID] = schools
    with open('result/{}.json'.format(areaID), 'w') as outfile:
        json.dump(result, outfile)'''

    done += 1
    print('progress: {}/{}'.format(done, len(areaIDs)))

db.commit()

print('FINISH!')