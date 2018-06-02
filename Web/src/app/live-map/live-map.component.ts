import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import * as L from 'leaflet';
import { FeatureCollection } from 'geojson';
import * as californiaJsonFile from 'assets/california.json';
import * as newYorkJsonFile from 'assets/new-york.json';

@Component({
  selector: 'app-live-map',
  templateUrl: './live-map.component.html',
  styleUrls: ['./live-map.component.css']
})
export class LiveMapComponent implements OnInit {
  @ViewChild('leafletDom') leafletDom: ElementRef;
  private map: L.Map;
  private customIcon: L.Icon;

  constructor() { }

  ngOnInit() {
    this.map = new L.Map(this.leafletDom.nativeElement).setView([38.6180521,-99.6654538], 3);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
      maxZoom: 18,
      attribution: '',
      id: 'mapbox.streets'
    }).addTo(this.map);

    const CustomIcon = L.Icon.extend({
      options: {
        iconUrl: 'assets/marker-icon.png',
        iconRetinaUrl: 'assets/marker-icon-2x.png',
        shadowUrl: 'assets/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        tooltipAnchor: [16, -28],
        shadowSize: [41, 41]
      }
    });

    this.customIcon = new CustomIcon();

    this.initStatesMarkers();
  }

  private initStatesMarkers(): void {
    const californiaGeoJson: FeatureCollection = <any>californiaJsonFile as FeatureCollection;
    L.geoJSON(californiaGeoJson).addTo(this.map);
    const californiaMarker = L.marker([36.778261, -119.41793239999998], { icon: this.customIcon })
      .addTo(this.map)
      .bindPopup('A pretty CSS3 popup.<br> Easily customizable.');


    const newYorkGeoJson: FeatureCollection = <any>newYorkJsonFile as FeatureCollection;
    L.geoJSON(newYorkGeoJson).addTo(this.map);
    const newYorkMarker = L.marker([43.2994285, -74.2179326], { icon: this.customIcon })
      .addTo(this.map)
      .bindPopup('A pretty CSS3 popup.<br> Easily customizable.');
  }
}
