import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class APIService {
  API_URL: string = "/transcribe";
  constructor(private http: HttpClient) { }

  getTranslation(data:FormData): Observable<string> {
    const url = `${this.API_URL}`;
    return this.http.post<string>(url, data, {responseType: 'text' as 'json'});
  }
}
