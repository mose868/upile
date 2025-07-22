'use client';
import React from 'react';
import { useGetAdminData } from '../../hooks/useGetAdminData';
import AdminChart from '../../Chart/admin';
import Layout from './components/Layout';

const AdminDashboard = () => {
  const { metrics, isLoading, error } = useGetAdminData(); 

  if (isLoading) {
    return <p>Loading ...</p>;
  }

  if (error) {
    return <p>Error: {error.message}</p>;
  }

  const totalPoliceStations = metrics?.TotalPoliceStations ?? 0;
  const totalMortuaries = metrics?.TotalMortuaries ?? 0;
  const successfulMatches = metrics?.SuccessfulMatches ?? 0;  

  return (
    <Layout>
      <div className="min-h-screen w-full flex flex-col bg-gray-100 px-2 sm:px-4 md:px-8 py-4">
        <div className="container mx-auto">
          <div className="flex flex-col md:flex-row flex-wrap gap-4 md:gap-8 mt-6 justify-center items-stretch">
            <div className="bg-[#D4B337] text-[#FFFFFF] text-center text-lg sm:text-xl md:text-2xl font-bold p-4 sm:p-6 rounded-lg shadow-md w-full max-w-xs flex-1">
              Total Police Stations: <br/>
              <span className="text-2xl sm:text-3xl md:text-4xl">{totalPoliceStations}</span>
            </div>
            <div className="bg-[#662113] text-[#FFFFFF] text-center text-lg sm:text-xl md:text-2xl font-bold p-4 sm:p-6 rounded-lg shadow-md w-full max-w-xs flex-1">
              Total Mortuaries: <br/>
              <span className="text-2xl sm:text-3xl md:text-4xl">{totalMortuaries}</span>
            </div>
            <div className="bg-[#8D4004] text-[#FFFFFF] text-center text-lg sm:text-xl md:text-2xl font-bold p-4 sm:p-6 rounded-lg shadow-md w-full max-w-xs flex-1">
              Successful Matches: <br/>
              <span className="text-2xl sm:text-3xl md:text-4xl">{successfulMatches}</span>
            </div>
          </div>
          <div className="mt-8 flex flex-col items-center">
            <div className="w-full max-w-3xl">
              <AdminChart/>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default AdminDashboard;
