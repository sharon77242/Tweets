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

  displayStateLoading = false;

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

    this.http.get('http://127.0.0.1:5000/' + this.generateForm.controls.state).subscribe((res: Response) => {
      this.timesList = JSON.parse(res.text());
      console.log(JSON.parse(res.text()));

      this.displayStateLoading = false;
      this.generateForm.controls.state.enable();
    });
  }

  Generate(): void {
    if (this.generateForm.invalid) {

    } else {
      this.http.post('http://127.0.0.1:5000/', {
        country: this.generateForm.controls.state,
        time: this.generateForm.controls.time
      }).subscribe((res: Response) => {
        console.log(JSON.parse(res.text()));
      });
    }
  }

}
