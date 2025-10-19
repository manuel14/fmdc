// mapa.js
// Receives: selectors for map, modal, videoContainer, closeModal, and videoUrls object

function initMapa({
  mapDiv,
  modal,
  videoContainer,
  closeModal,
  videoUrls,
  geojsonUrl,
  menuItemSelector,
}) {
  const mapId = mapDiv.id;
  const map = L.map(mapId);
  let originalZoom;

  // Modal close logic
  function closeModalHandler() {
    if (modal.classList) {
      modal.classList.remove("active");
    }
    modal.style.display = "none";
    videoContainer.innerHTML = "";
  }
  if (closeModal) {
    closeModal.onclick = function (e) {
      closeModalHandler();
    };
  }
  // Close modal when clicking outside the modal content
  if (modal) {
    modal.addEventListener("click", function (event) {
      // Only close if clicking directly on the modal background, not its children
      if (event.target === modal) {
        closeModalHandler();
      }
    });
  }

  const departmentColors = {
    "alvear": "#C0F2F3",
    "bella vista": "#BE94E8",
    "beron de astrada": "#F2FFAB",
    "caa catí": "#E595AB",
    "corrientes": "#F3D9AC",
    "concepcion": "#C0F2F3",
    "curuzu cuatia": "#DB946E",
    "empedrado": "#FCFF9F",
    "esquina": "#FFFFB5",
    "goya": "#FFD4A7",
    "itati": "#C7CEFF",
    "ituzaingo": "#F69FF8",
    "lavalle": "#A8DDAE",
    "la cruz": "#DAE1FF",
    "mburucuya": "#AAFF9E",
    "mercedes": "#FFEE8E",
    "monte caseros": "#D5ECF1",
    "paso de los libres": "#C8C4D1",
    "san cosme": "#E595AB",
    "san luis del palmar": "#D3FFDA",
    "santo tome": "#F6CECF",
    "san roque": "#EE96DE",
    "saladas": "#C2BDCE",
    "santo tome": "#E5DC72",
    "san roque": "#EEB6B6",
    "sauce": "#FFEF79",
    "san miguel": "#B8ACFB"
  }

  const tooltipOffsets = {
    alvear: [55, 80],
    "bella vista": [-20, 30],
    "beron de astrada": [50, -10],
    corrientes: [-30, 20],
    "curuzu cuatia": [0, 25],
    empedrado: [0, 40],
    goya: [0, -30],
    itati: [0, 0],
    ituzaingo: [0, -30],
    "la cruz": [0, 50],
    mburucuya: [0, 30],
    mercedes: [-10, 50],
    "monte caseros": [0, 30],
    "paso de los libres": [0, 50],
    "san cosme": [10, 0],
    "san luis del palmar": [0, 20],
    "santo tome": [0, 20],
    saladas: [0, 35],
    "santo tome": [20, 90],
    "san roque": [0, 0],
    sauce: [0, 45],
    "san miguel": [0, 50],
  };

  fetch(geojsonUrl)
    .then((response) => response.json())
    .then((data) => {
      const geoJsonLayer = L.geoJSON(data, {
        style: {
          color: "#2c3e50",
          weight: 1,
          fillColor: "#FFEFB6",
          fillOpacity: 1,
          weight: 1.5,
          opacity: 0.1,
          interactive: true,
          bubblingMouseEvents: true,

        },
        pointToLayer: function (feature, latlng) {
          if (window.innerWidth > 425) {
            // Desktop marker (transparent via CSS)
            return L.marker(latlng, {
              icon: L.divIcon({
                className: "department-label department-label-transparent",
                html: `<div><span><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"23\" height=\"23\" viewBox=\"0 0 23 23\" fill=\"none\"><g clip-path=\"url(#clip0_298_16240)\"><path d=\"M19.8534 9.73624C19.8534 16.3526 11.4182 22.0238 11.4182 22.0238C11.4182 22.0238 2.98291 16.3526 2.98291 9.73624C2.98291 7.48011 3.87162 5.31639 5.45354 3.72106C7.03546 2.12574 9.18101 1.22949 11.4182 1.22949C13.6554 1.22949 15.8009 2.12574 17.3828 3.72106C18.9647 5.31639 19.8534 7.48011 19.8534 9.73624Z" stroke=\"#071739\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><path d=\"M11.4182 12.5716C12.9711 12.5716 14.23 11.302 14.23 9.73597C14.23 8.16992 12.9711 6.90039 11.4182 6.90039C9.86531 6.90039 8.60645 8.16992 8.60645 9.73597C8.60645 11.302 9.86531 12.5716 11.4182 12.5716Z" stroke=\"#071739\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></g><defs><clipPath id=\"clip0_298_16240\"><rect width=\"22.494\" height=\"22.6847\" transform=\"translate(0.171387 0.28418)\"/></clipPath></defs></svg></span></div>`,
              }),
            });
          }
        },
        onEachFeature: function (feature, layer) {
          let name = feature.properties.name
            ?.split(" ")
            .join("")
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase();
          if (
            feature.properties &&
            feature.properties.name &&
            feature.geometry.type !== "Point"
          ) {
            const deptName =
              feature.properties && feature.properties.name
                ? feature.properties.name.toLowerCase()
                : null;
            const offset = tooltipOffsets[deptName] || [0, 20];
            if (window.innerWidth < 1440) {
              layer.bindTooltip(
                `<span style="font-family: Montserrat; font-weight: 700; font-size: 8px; padding: 2px 6px;">${deptName.toUpperCase()}</span>`,
                {
                  permanent: true,
                  direction: "center",
                  className: "polygon-label",
                  offset: [0, 0],
                  interactive: true,
                  bubblingMouseEvents: true,
                }
              );
              layer.setStyle({
                fillColor: departmentColors[deptName],
              })
            } else {
              layer.bindTooltip(
                `<span style="font-family: Montserrat;font-weight: 700; font-size: 14px; padding: 2px 6px;">${feature.properties.name.toUpperCase()}</span>`,
                {
                  permanent: true,
                  direction: "center",
                  className: "polygon-label",
                  interactive: false,
                  offset: offset,
                }
              );
              layer.setStyle({
                fillColor: departmentColors[deptName],
              })
            }
            const videoUrl = videoUrls[name];
            layer.on("click", function () {
              if (videoUrl) {
                modal.style.display = "block";
                videoContainer.innerHTML = `<video width="100%" height="100%" controls><source src="${videoUrl}" type="video/mp4">Your browser does not support the video tag.</video>`;
              }
            });
            layer.on("mouseover", function (e) {
              this.setStyle({
                color: "#A4B5C4",
                weight: 3,
                fillColor: departmentColors[deptName],
              });
              if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                this.bringToFront();
              }
            });

          }
          if (
            feature.geometry.type === "Point" &&
            feature.properties &&
            feature.properties.name &&
            videoUrls[name]
          ) {
            const videoUrl = videoUrls[name];
            layer.on("click", function () {
              if (videoUrl) {
                modal.style.display = "block";
                videoContainer.innerHTML = `<video controlsList="nodownload" width="100%" height="100%" controls><source src="${videoUrl}" type="video/mp4">Your browser does not support the video tag.</video>`;
              }
            });
          }
        },
      }).addTo(map);
      const bounds = geoJsonLayer.getBounds();
      map.setMaxZoom(14);
      const paddedBounds = bounds.pad(0.1);
      map.setMaxBounds(paddedBounds);
      map.fitBounds(bounds);
      if (window.innerWidth <= 320) {
        let higherZoom = Math.max(map.getZoom(), 6.4);
        map.setZoom(higherZoom);
        map.setMinZoom(higherZoom);
      }
      else if (window.innerWidth <= 425) {
        let higherZoom = Math.max(map.getZoom(), 7);
        map.setZoom(higherZoom);
        map.setMinZoom(higherZoom);
      } else if (window.innerHeight <= 1024) {
        let higherZoom = Math.max(map.getZoom(), 7.4);
        map.setZoom(higherZoom);
        map.setMinZoom(higherZoom);
      } else {
        map.fitBounds(bounds);
        originalZoom = map.getZoom();
        map.setMinZoom(originalZoom);
        map.on("drag", function () {
          map.panInsideBounds(paddedBounds, { animate: false });
        });
      }
    });

  // Dropdown menu video click (mobile)
  document.querySelectorAll(menuItemSelector).forEach(function (item) {
    item.addEventListener("click", function (event) {
      let name = this.getAttribute("data-name");
      const videoUrl =
        videoUrls[name] ||
        videoUrls[name && name.toUpperCase()] ||
        videoUrls[name && name.toLowerCase()];
      if (videoUrl) {
        modal.style.display = "block";
        videoContainer.innerHTML = `<video controlsList="nodownload" width="100%" height="100%" controls preload="none"><source src="${videoUrl}" type="video/mp4">Your browser does not support the video tag.</video>`;
      }
    });
  });

  // Ensure the map resizes correctly after all layout/rendering is done
  window.addEventListener("load", function () {
    setTimeout(function () {
      if (typeof map !== "undefined" && map.invalidateSize) {
        map.invalidateSize();
      }
    }, 100);
  });
}
