import { Routes } from '@angular/router';
import { TripListingComponent } from './trip-listing/trip-listing';
import { AddTrip } from './add-trip/add-trip';
import { EditTrip } from './edit-trip/edit-trip';
import { Login } from './login/login';
import { adminAuthGuard } from './auth.guard';

export const routes: Routes = [
  { path: '', component: TripListingComponent },
  { path: 'add-trip', component: AddTrip, canActivate: [adminAuthGuard] },
  { path: 'edit-trip/:tripCode', component: EditTrip, canActivate: [adminAuthGuard] },
  { path: 'login', component: Login }
];
