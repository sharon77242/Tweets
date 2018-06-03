import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';

@Injectable({
  providedIn: 'root'
})
export class TweetsService {
  private static statesList: Array<{ label: string, value: string }>;
  private readonly SERVER_URL = 'http://193.106.55.145:8080/';

  constructor(private httpService: Http) { }

  GetStatesList(): Array<{ label: string, value: string }> {
    TweetsService.statesList = [
      { label: 'New York (NY)', value: 'new_york' },
      { label: 'California (CA)', value: 'california' },
      { label: 'Los Angeles (LA)', value: 'los_angeles' }
    ];

    return TweetsService.statesList;
  }

  GetStateTweetsTimes(
    stateName: string,
    successCallback: (timesList: Array<string>) => void,
    errorCallback?: () => void
  ): void {
    this.httpService.get(this.SERVER_URL + stateName).subscribe((res: Response) => {
      const result = JSON.parse(res.text());

      if (!(result[0] + '').includes('ERROR')) {
        for (let i = 0; i < result.length; i++) {
          result[i] = result[i].split('.')[0];
        }

        successCallback(result);
      } else {
        if (errorCallback) {
          errorCallback();
        }
      }
    });
  }

  GetTweet(stateName: string, time: string, successCallback: (generatedResult: string) => void): void {
    this.httpService.post(this.SERVER_URL, {
      country: stateName,
      time: time
    }).subscribe((res: Response) => {
      successCallback(res.text());
    });
  }
}
