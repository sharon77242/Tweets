import { Component, OnInit } from '@angular/core';
import { Validators, FormBuilder, FormGroup, FormControl } from '@angular/forms';
import { TweetsService } from '../services/tweets.service';

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

  constructor(private tweetService: TweetsService) {
    this.statesList = tweetService.GetStatesList();
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
    this.DisableForm();
    this.stateSelectionError = '';
    this.timesList = [];
    this.generateForm.controls.time.setValue('');
    this.generateForm.controls.time.disable();

    this.tweetService.GetStateTweetsTimes(
      this.generateForm.controls.state.value,
      (timesList: Array<string>): void => {
        this.timesList = timesList;
        this.EnableForm();
      },
      (): void => {
        this.stateSelectionError = 'Error. No available tweets for the state';
        this.EnableForm();
      });
  }

  private DisableForm(): void {
    this.displayStateLoading = true;
    this.generateForm.controls.state.disable();
  }

  private EnableForm(): void {
    this.displayStateLoading = false;
    this.generateForm.controls.state.enable();
  }

  Generate(): void {
    if (this.generateForm.invalid) {
      this.shouldShakeButton = true;

      setTimeout(() => {
        this.shouldShakeButton = false;
      }, 1000);
    } else {
      this.tweetService.GetTweet(
        this.generateForm.controls.state.value,
        this.generateForm.controls.time.value,
        (generatedResult: string) => {
          this.shouldAnimateForm = true;
          this.generatedResult = generatedResult;
          
          setTimeout(() => {
            this.shouldHideForm = true;
            this.shouldDisplayGeneratedResult = true;
          }, 1000);
        }
      );
    }
  }

}
