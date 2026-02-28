import type { ChangeEvent } from 'react';
import { LocationSearch } from './LocationSearch';

export type BirthData = {
  date: string;
  time: string;
  latitude: string;
  longitude: string;
}

interface BirthDataFormProps {
  data: BirthData;
  onChange: (data: BirthData) => void;
  label?: string;
  errors?: Partial<Record<keyof BirthData, string>>;
}

export const BirthDataForm = ({ data, onChange, label, errors = {} }: BirthDataFormProps) => {
  const handleChange = (field: keyof BirthData) => (e: ChangeEvent<HTMLInputElement>) => {
    onChange({ ...data, [field]: e.target.value });
  };

  const inputClass = "w-full bg-[#1a1a24] border border-[#2a2a3a] rounded-lg px-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:border-[#8b5cf6] transition-colors";
  const errorClass = "border-red-500 focus:border-red-500";
  const labelClass = "block text-sm font-medium text-gray-300 mb-2";
  const errorTextClass = "text-red-400 text-xs mt-1";

  return (
    <div className="space-y-4 p-6 bg-[#0f0f14] border border-[#2a2a3a] rounded-xl">
      {label && <h3 className="text-lg font-semibold text-[#8b5cf6] mb-4">{label}</h3>}
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className={labelClass}>Date of Birth</label>
          <input
            type="date"
            value={data.date}
            onChange={handleChange('date')}
            className={`${inputClass} ${errors.date ? errorClass : ''}`}
          />
          {errors.date && <p className={errorTextClass}>{errors.date}</p>}
        </div>

        <div>
          <label className={labelClass}>Time of Birth</label>
          <input
            type="time"
            value={data.time}
            onChange={handleChange('time')}
            className={`${inputClass} ${errors.time ? errorClass : ''}`}
          />
          {errors.time && <p className={errorTextClass}>{errors.time}</p>}
        </div>
      </div>

      <div>
        <label className={labelClass}>Birth Location</label>
        <LocationSearch
          onSelect={(lat, lon, name) => {
            onChange({ 
              ...data, 
              latitude: lat.toString(), 
              longitude: lon.toString() 
            });
          }}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className={labelClass}>Latitude</label>
          <input
            type="text"
            value={data.latitude}
            onChange={handleChange('latitude')}
            placeholder="e.g., 40.7128"
            className={`${inputClass} ${errors.latitude ? errorClass : ''}`}
            readOnly
          />
          {errors.latitude && <p className={errorTextClass}>{errors.latitude}</p>}
        </div>

        <div>
          <label className={labelClass}>Longitude</label>
          <input
            type="text"
            value={data.longitude}
            onChange={handleChange('longitude')}
            placeholder="e.g., -74.0060"
            className={`${inputClass} ${errors.longitude ? errorClass : ''}`}
            readOnly
          />
          {errors.longitude && <p className={errorTextClass}>{errors.longitude}</p>}
        </div>
      </div>
    </div>
  );
};
