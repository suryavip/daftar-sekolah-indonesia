import requests
import json

# mengumpulkan areaIDs (kode_wilayah) dari http://jendela.data.kemdikbud.go.id/api/index.php/cwilayah/wilayahKabGet

r = requests.get('http://jendela.data.kemdikbud.go.id/api/index.php/cwilayah/wilayahKabGet')
if r.status_code != 200:
    raise Exception('Gagal mengumpulkan kode_wilayah ({})'.format(r.status_code))

areas = r.json()['data']

areaIDs = [area['kode_wilayah'].strip() for area in areas]
# https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
# print(areaIDs)

# mengumpulkan detail sekolah dari http://jendela.data.kemdikbud.go.id/api/index.php/Csekolah/detailSekolahGET?mst_kode_wilayah=XXXXXX

done = 0
for areaID in areaIDs:
    r = requests.get('http://jendela.data.kemdikbud.go.id/api/index.php/Csekolah/detailSekolahGET?mst_kode_wilayah={}'.format(areaID))
    if r.status_code != 200:
        raise Exception('Gagal mengumpulkan data sekolah untuk kode_wilayah {} ({})'.format(areaID, r.status_code))

    schools = r.json()['data']

    result = {}
    result[areaID] = schools
    with open('result/{}.json'.format(areaID), 'w') as outfile:
        json.dump(result, outfile)

    done += 1
    print('progress: {}/{}'.format(done, len(areaIDs)))

print('FINISH!')