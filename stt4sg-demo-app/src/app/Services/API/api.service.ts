import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import {Observable} from "rxjs";
import { HttpEvent } from '@angular/common/http';

export interface Rating {
  rating: number;
}

export interface Transcription {
  id: string;
  created: string;
  audio_file: string;
  transcription: string;
  ratings: Rating[];
}

export interface Progress {
  current_step: number;
  steps: number;
  step_description: string;
}

export interface Status {
  id: string;
  job_status: string;
  progress: Progress;
}

@Injectable({
  providedIn: 'root'
})
export class APIService {
  API_URL: string = "https://stt4sg.fhnw.ch/api";
  constructor(private http: HttpClient) { }

  getTranslation(audio: Blob): Observable<Transcription> {
    const url = `${this.API_URL + '/transcribe/'}`;
    const data = new FormData();
    data.append('audio_file', audio, "audio.wav");
    return this.http.post<Transcription>(url, data);
  }

  submitRating(id: string, rating: Rating): Observable<Transcription> {
    const url = `${this.API_URL + '/transcription/' + id + '/rate/'}`;
    const options = {headers: {'Content-Type': 'application/json'}};
    return this.http.post<Transcription>(url, JSON.stringify(rating), options);
  }

  longStatus(id: string): Observable<Status> {
    const url = `${this.API_URL + '/long-status/' + id}`;
    return this.http.get<Status>(url)
  }

  upload(audio: Blob, fileName: string): Observable<HttpEvent<Status>> {
    const url = `${this.API_URL + '/transcribe-long/'}`;
    const data = new FormData();
    data.append('file', audio, fileName);
    return this.http.post<Status>(url, data, { reportProgress: true, observe: 'events' });
  }
}
