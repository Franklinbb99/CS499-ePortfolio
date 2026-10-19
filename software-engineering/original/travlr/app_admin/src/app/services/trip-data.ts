import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Trip } from '../models/trip';
import { Auth } from './auth';
import { User } from '../models/user';
import { AuthResponse } from '../models/auth-response';

@Injectable({
  providedIn: 'root'
})
export class TripDataService {

  private apiUrl = 'http://localhost:3000/api/trips';

  constructor(
   private http: HttpClient,
   private auth: Auth
) {}

  public getTrips(): Observable<Trip[]> {
    const headers = new HttpHeaders({
      'Cache-Control': 'no-cache',
      'Pragma': 'no-cache'
    });
    return this.http.get<Trip[]>(this.apiUrl, { headers });
  }
  public getTrip(tripCode: string): Observable<Trip> {
    return this.http.get<Trip>(this.apiUrl + '/' +tripCode);
  }

  public addTrip(trip: Trip): Observable<Trip> {

  const headers = new HttpHeaders({
    'Authorization': 'Bearer ' + this.auth.getToken()
  });

  return this.http.post<Trip>(this.apiUrl, trip, { headers });

}

  public updateTrip(trip: Trip): Observable<Trip> {

  const headers = new HttpHeaders({
    'Authorization': 'Bearer ' + this.auth.getToken()
  });

  return this.http.put<Trip>(

    this.apiUrl + '/' + trip.code,

    trip,

    { headers }

  );

}

  public login(user: User, passwd: string): Observable<AuthResponse> {

  const formData = {

    name: user.name,

    email: user.email,

    password: passwd

  };

  return this.http.post<AuthResponse>(

    'http://localhost:3000/api/login',

    formData

  );

}


}