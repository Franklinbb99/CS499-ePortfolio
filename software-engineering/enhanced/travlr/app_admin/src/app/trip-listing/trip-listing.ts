import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TripCardComponent } from '../trip-card/trip-card';
import { TripDataService } from '../services/trip-data';
import { Router } from '@angular/router';
import { AuthenticationService } from '../authentication';
import { Trip } from '../models/trip';

@Component({
  selector: 'app-trip-listing',
  standalone: true,
  imports: [CommonModule, FormsModule, TripCardComponent],
  templateUrl: './trip-listing.html',
  styleUrl: './trip-listing.css',
})
export class TripListingComponent implements OnInit {
  trips: Trip[] = [];
  searchTerm = '';
  isLoading = true;
  loadError = '';

  constructor(
    private tripService: TripDataService,
    private router: Router,
    private authenticationService: AuthenticationService
  ) {}

  ngOnInit(): void {
    this.tripService.getTrips().subscribe({
      next: (data: Trip[]) => {
        this.trips = data;
        this.isLoading = false;
      },
      error: () => {
        this.loadError = 'Trip information could not be loaded. Please try again later.';
        this.isLoading = false;
      }
    });
  }

  public get filteredTrips(): Trip[] {
    const query = this.searchTerm.trim().toLocaleLowerCase();

    if (!query) {
      return this.trips;
    }

    return this.trips.filter((trip) =>
      [trip.name, trip.code, trip.resort]
        .some((value) => value?.toLocaleLowerCase().includes(query))
    );
  }

  public addTrip(): void {
    this.router.navigate(['add-trip']);
  }

  public isLoggedIn(): boolean {
    return this.authenticationService.isLoggedIn();
  }
}

