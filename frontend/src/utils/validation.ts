import type { BirthData } from '../components/forms/BirthDataForm';

export const validateBirthData = (data: BirthData): Partial<Record<keyof BirthData, string>> => {
  const errors: Partial<Record<keyof BirthData, string>> = {};

  if (!data.date) {
    errors.date = 'Date is required';
  }

  if (!data.time) {
    errors.time = 'Time is required';
  }

  const lat = parseFloat(data.latitude);
  if (!data.latitude || isNaN(lat) || lat < -90 || lat > 90) {
    errors.latitude = 'Please search for a location above';
  }

  const lon = parseFloat(data.longitude);
  if (!data.longitude || isNaN(lon) || lon < -180 || lon > 180) {
    errors.longitude = 'Please search for a location above';
  }

  return errors;
};
