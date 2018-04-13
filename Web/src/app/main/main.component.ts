import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {
  showDocuments = false;
  showArrow = false;
  showText = false;

  constructor() {
  }

  ngOnInit() {
    setTimeout(() => {
      this.showDocuments = true;
    }, 500);

    setTimeout(() => {
      this.showArrow = true;
    }, 1000);

    setTimeout(() => {
      this.showText = true;
    }, 1500);
  }

}
