import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-generate',
  templateUrl: './generate.component.html',
  styleUrls: ['./generate.component.css']
})
export class GenerateComponent implements OnInit {
  statesList: Array<{ label: string, value: string }>;
  selectedState: string;

  constructor() {
    this.selectedState = '';

    this.statesList = [
      { label: 'New York', value: 'NY' },
      { label: 'California', value: 'CA' },
    ];
  }

  ngOnInit() {
  }

}
