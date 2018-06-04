import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import * as L from 'leaflet';
import { FeatureCollection } from 'geojson';
import * as californiaJsonFile from 'assets/california.json';
import * as newYorkJsonFile from 'assets/new-york.json';
import { TweetsService } from '../services/tweets.service';
import { DateFormatPipe } from '../pipes/date-format.pipe';
import { StateModel } from '../models/state.model';

@Component({
  selector: 'app-live-map',
  templateUrl: './live-map.component.html',
  styleUrls: ['./live-map.component.css']
})
export class LiveMapComponent implements OnInit {
  @ViewChild('leafletDom') leafletDom: ElementRef;
  private map: L.Map;
  private customIcon: L.Icon;

  private statesList: Array<{ label: string, value: string }>;
  private statesCoordinates: any;

  constructor(private tweetsService: TweetsService, private dateFormatPipe: DateFormatPipe) {
    this.statesList = tweetsService.GetStatesList();
    this.statesCoordinates = {};

    // New York
    this.statesCoordinates[this.statesList[0].value] = new StateModel([43.2994285, -74.2179326]);

    // California
    this.statesCoordinates[this.statesList[1].value] = new StateModel([36.504750, -119.768142]);

    // Los Angeles
    this.statesCoordinates[this.statesList[2].value] = new StateModel([34.052235, -118.243683]);
  }

  ngOnInit() {
    this.map = new L.Map(this.leafletDom.nativeElement).setView([38.6180521, -99.6654538], 3);

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
      maxZoom: 18,
      attribution: '',
      id: 'mapbox.streets'
    }).addTo(this.map);

    const CustomIcon = L.Icon.extend({
      options: {
        iconUrl: 'assets/marker-icon-new.png',
        iconRetinaUrl: 'assets/marker-icon-2x-new.png',
        shadowUrl: 'assets/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        tooltipAnchor: [16, -28],
        shadowSize: [41, 41]
      }
    });

    this.customIcon = new CustomIcon();

    this.initStatesPolygons();
  }

  private initStatesPolygons(): void {
    const californiaGeoJson: FeatureCollection = <any>californiaJsonFile as FeatureCollection;
    L.geoJSON(californiaGeoJson).addTo(this.map);

    const newYorkGeoJson: FeatureCollection = <any>newYorkJsonFile as FeatureCollection;
    L.geoJSON(newYorkGeoJson).addTo(this.map);

    this.initStatesMarkers();

    setInterval(this.initStatesMarkers.bind(this), 10000);
  }

  private initStatesMarkers(): void {
    for (const state of this.statesList) {
      this.tweetsService.GetStateTweetsTimes(
        state.value,
        (timesList: Array<string>): void => {
          this.tweetsService.GetTweet(state.value, timesList[0], (generatedResult: string): void => {
            this.createMarkerForState(
              generatedResult,
              state.label,
              this.dateFormatPipe.transform(timesList[0]),
              state.value,
              this.statesCoordinates[state.value].coords
            );
          });
        }
      );
    }
  }

  private markerClicked(event: any): void {
    event.originalEvent.path[0].src = 'assets/marker-icon-2x.png';
  }

  private createMarkerForState(text: string, stateName: string, time: string, stateValue: string, coords: Array<number>): void {
    const currentState = this.statesCoordinates[stateValue];

    if (currentState.marker) {
      if (currentState.time && currentState.time  === time) {
        return;
      }

      this.map.removeLayer(this.statesCoordinates[stateValue].marker);
    }

    const marker = L.marker([coords[0], coords[1]], { icon: this.customIcon })
      .addTo(this.map)
      .on('click', this.markerClicked)
      .bindPopup(`<strong>${stateName}</strong><br>${text}<br><br>${time}`);

    this.statesCoordinates[stateValue].marker = marker;
    this.statesCoordinates[stateValue].time = time;
  }
}
