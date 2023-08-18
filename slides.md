---
theme: seriph
background: https://source.unsplash.com/collection/94734566/1920x1080
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## Slidev Starter Template
  Presentation slides for developers.

  Learn more at [Sli.dev](https://sli.dev)
drawings:
  persist: false
transition: slide-left
title: Carto Support Engineer Test
---

# Carto Lead Support Engineer Test

Results using [Sli.dev](https://sli.dev/)

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-2 py-1 rounded cursor-pointer" hover="bg-white bg-opacity-10">
    Press Space for next page <carbon:arrow-right class="inline"/>
  </span>
</div>

<div class="abs-br m-6 flex gap-2">
  <button @click="$slidev.nav.openInEditor()" title="Open in Editor" class="text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white">
    <carbon:edit />
  </button>
  <a href="https://github.com/slidevjs/slidev" target="_blank" alt="GitHub"
    class="text-xl slidev-icon-btn opacity-50 !border-none !hover:text-white">
    <carbon-logo-github />
  </a>
</div>

<!--
The last comment block of each slide will be treated as slide notes. It will be visible and editable in Presenter Mode along with the slide. [Read more in the docs](https://sli.dev/guide/syntax.html#notes)
-->

---
transition: fade-out
---

# 1.- Warming up with two support

## Popups not working

Although your code seems right, I've found you probably have forgot setting up the content's popup by using
`popup.setContent(content)`

```js {all|73} {lines:true, startLine:67}
  // My popup up content
  content += `<h3> ${data.name} </h3>`;
  content += `<p>Between ${data.pop_min} and ${data.pop_max} inhabitants </p>`;
  content += `</div>`;

  popup.setLatLng(featureEvent.latLng);
  popup.setContent(content)
  if (!popup.isOpen()) {
    popup.openOn(map);
  }
```

<arrow v-click="1" x1="550" y1="120" x2="330" y2="330" color="#564" width="3" arrowSize="1" />

You can find out more at [popup's Leaflet methods documentation](https://leafletjs.com/reference.html#popup-setcontent), and review the full code [Here](./popups.html)


<br>
<br>


---
transition: fade-out
---

## Query doubt

```sql
SELECT e.name,
      count(*) AS counts,
      sum(p.population) as population
FROM european_countries e
JOIN populated_places p
ON ST_Intersects(p.the_geom, e.the_geom)
GROUP BY e.name
```

Related to your query. It's a common geospatial query, based on postgis. 
It's working about two tables, `populated_places` and `european_countries`, both have geometries:
- populated_places probably will be points
- european_countries probably will be polygons (or multypolygons)

The query It's telling you the next information:
- The name of the Country
- How many populated_places falls into each country geometry
- The total population for each Country (based on the sum of population of each populated place)

---
---

### Related info

Information about `ST_intersects` function from PostGIS [can be found here](https://postgis.net/docs/en/ST_Intersects.html). It's not trivial how we intersects geometries, so It's important to understand how does it works.





---
---

#  2.- Python Support Engineer

I've built a MVP for a ETL routine. It can transfer to carto both geojson requests and csv file. 
In order to put it into Production we will need to update to get from cli argument which colum from csv file has the geometry. 
If we want to accept multipart requests with geospatial files (such as csv ,geoparquet or shapefiles) we need to improve the code. 

It's just a basic Carto Data loader solution

You can find info about how to run it [In the markdown file](./python/readme.md) but it's basically:

`python ./python/main.py {yourRelativeOrAbsoultePath} {yourGeoJsonRequest}`

---
---

# 3.- Docker Support Engineer



⚠⚠ [Instead of screenshots, I've used Loom](https://www.loom.com/share/eb69567b7cd64ea6921b8085ebb87471?sid=c436ccb7-0f43-47e2-8597-b7b694aea9ad) ⚠⚠

> Finally i've included [some screenshots](./screenshots/) to facilitate the review

#### Raise up a virtual machine

`docker run --rm -it --entrypoint bash ubuntu`

#### Prerequisites

```bash
# We need to install some common libraries to install docker (It depends on your machine OS)
apt update && apt install lsb-core -y && \
apt-get -y install sudo && \
sudo apt upgrade -y && \
sudo apt update && \
sudo apt install software-properties-common -y
```

---
---

#### Installing docker

```bash
# We update our packages and add the GPG key for the official Docker repository to our system 
sudo apt update && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# Then we add the Docker repository to our sources:
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" -y 
# Finally, we install docker 
sudo apt install docker-ce -y
# We can check now if Docker Engine it's working
docker --version
```


#### About Docker-Compose
```bash
# We download it from source
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# We make it executable
sudo chmod +x /usr/local/bin/docker-compose
# We check it 
docker-compose --version
```

---
---

### Start Postgres 12 Instance using Docker-compose

⚠⚠ [Another Loom video to explain (Spanish Alert)](https://www.loom.com/share/d2112bef579b406784e949e7124249c2?sid=6b671b99-2566-4803-b1fc-9e7516fbc9cc) ⚠⚠

```yaml
version: '3.3'

services:
  postgis:
    image: postgres:12.16-bullseye
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=admin
    ports:
      - '5432:5432'
    volumes: 
      - db:/var/lib/postgresql/data

volumes:
  db:
    driver: local
```

### Check docker volume location
`docker volume inspect carto_test_db`