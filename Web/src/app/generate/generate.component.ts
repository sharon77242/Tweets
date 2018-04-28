import { Component, OnInit } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Validators, FormBuilder, FormGroup, FormControl } from '@angular/forms';

@Component({
  selector: 'app-generate',
  templateUrl: './generate.component.html',
  styleUrls: ['./generate.component.css']
})
export class GenerateComponent implements OnInit {
  statesList: Array<{ label: string, value: string }>;
  timesList: Array<string>;
  generateForm: FormGroup;

  shouldHideForm = false;
  shouldAnimateForm = false;
  shouldShakeButton = false;
  shouldDisplayGeneratedResult = false;
  displayStateLoading = false;
  stateSelectionError = '';
  generatedResult = '';

  constructor(private http: Http) {
    this.statesList = [
      { label: 'New York (NY)', value: 'NewYork' },
      { label: 'California (CA)', value: 'California' },
      { label: 'Los Angeles (LA)', value: 'LosAngeles' }
    ];

    this.timesList = [];
  }

  ngOnInit() {
    this.generateForm = new FormGroup({
        name: new FormControl('', Validators.required),
        email: new FormControl('', [
            Validators.required,
            Validators.pattern('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$')
        ]),
        state: new FormControl('', Validators.required),
        time: new FormControl({ value: '', disabled: true }, Validators.required)
    });
  }

  StateChanged(): void {
    this.displayStateLoading = true;
    this.generateForm.controls.state.disable();
    this.stateSelectionError = '';
    this.timesList = [];
    this.generateForm.controls.time.setValue('');
    this.generateForm.controls.time.disable();

    this.http.get('http://127.0.0.1:5000/' + this.generateForm.controls.state.value).subscribe((res: Response) => {
      const timesList = JSON.parse(res.text());

      if (!(timesList[0] + '').includes('error')) {
        this.timesList = timesList;
        this.generateForm.controls.time.enable();
      } else {
        this.stateSelectionError = 'Error. No available tweets for the state';
      }

      this.displayStateLoading = false;
      this.generateForm.controls.state.enable();
    });
  }

  Generate(): void {
    if (this.generateForm.invalid) {
      this.shouldShakeButton = true;

      setTimeout(() => {
        this.shouldShakeButton = false;
      }, 1000);
    } else {
      this.http.post('http://127.0.0.1:5000/', {
        country: this.generateForm.controls.state.value,
        time: this.generateForm.controls.time.value
      }).subscribe((res: Response) => {
        this.shouldAnimateForm = true;
        this.generatedResult = res.text();

        setTimeout(() => {
          this.shouldHideForm = true;
          this.shouldDisplayGeneratedResult = true;
        }, 1000);
      });
    }
  }

}
