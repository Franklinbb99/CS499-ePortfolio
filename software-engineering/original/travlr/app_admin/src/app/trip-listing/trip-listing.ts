import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TripCardComponent } from '../trip-card/trip-card';
import { TripDataService } from '../services/trip-data';
import { Router } from '@angular/router';
import { AuthenticationService } from '../authentication';

@Component({
  selector: 'app-trip-listing',
  standalone: true,
  imports: [CommonModule, TripCardComponent],
  templateUrl: './trip-listing.html',
  styleUrl: './trip-listing.css',
})
export class TripListingComponent implements OnInit {
  trips: Array<any> = [];

  constructor(
    private tripService: TripDataService,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private authenticationService: AuthenticationService
  ) {}

  ngOnInit(): void {
    this.tripService.getTrips().subscribe({
      next: (data: any) => {
        this.trips = data;
        this.cdr.detectChanges(); 
        
      },
      error: (error: any) => {
        console.log('Error: ' + error);
      }
    })
  }

  public addTrip(): void {
    this.router.navigate(['add-trip']);
  }

  public isLoggedIn(): boolean {
    return this.authenticationService.isLoggedIn();
  }
}



