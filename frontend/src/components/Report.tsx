import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line
} from 'recharts';
import useTranslation from '../i18n/useTranslation';

interface ReportData {
  date?: string;
  start_date?: string;
  end_date?: string;
  total_flights: number;
  completed_flights: number;
  delayed_flights: number;
  on_time_percentage: number;
  average_delay_minutes: number;
  total_alerts?: number;
  competitor_stats?: Record<string, any>;
  daily_reports?: any[];
}

interface ReportProps {
  reportType: string;
  dateRange: string;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

const Report: React.FC<ReportProps> = ({ reportType, dateRange }) => {
  const { t } = useTranslation();
  const [report, setReport] = useState<ReportData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchReportData = async () => {
      try {
        setLoading(true);
        
        let endpoint = '';
        let params = {};
        
        // Determine which API endpoint to call based on reportType and dateRange
        if (reportType === 'daily') {
          endpoint = 'http://localhost:8000/api/reports/daily';
          
          if (dateRange === 'today') {
            const today = new Date().toISOString().split('T')[0];
            params = { date: today };
          } else if (dateRange === 'yesterday') {
            const yesterday = new Date();
            yesterday.setDate(yesterday.getDate() - 1);
            params = { date: yesterday.toISOString().split('T')[0] };
          }
        } else if (reportType === 'performance' || reportType === 'operational' || reportType === 'competitor') {
          // For now, we'll use the weekly report for these types
          endpoint = 'http://localhost:8000/api/reports/weekly';
          
          if (dateRange === 'week') {
            // Use default (last 7 days)
          } else if (dateRange === 'month') {
            const endDate = new Date();
            params = { end_date: endDate.toISOString().split('T')[0] };
          }
        }
        
        if (endpoint) {
          const response = await axios.get(endpoint, { params });
          setReport(response.data);
        } else {
          // Fallback to mock data if no matching endpoint
          const mockReport: ReportData = {
            date: '2025-03-01',
            total_flights: 15,
            completed_flights: 12,
            delayed_flights: 3,
            on_time_percentage: 80,
            average_delay_minutes: 22.5,
            total_alerts: 5,
            competitor_stats: {
              'MedFlight': { total: 8, completed: 7 },
              'AirMed': { total: 6, completed: 5 }
            },
            daily_reports: [
              { date: '2025-02-23', total_flights: 12, completed_flights: 10, delayed_flights: 2, on_time_percentage: 83 },
              { date: '2025-02-24', total_flights: 14, completed_flights: 11, delayed_flights: 3, on_time_percentage: 79 },
              { date: '2025-02-25', total_flights: 16, completed_flights: 14, delayed_flights: 2, on_time_percentage: 88 },
              { date: '2025-02-26', total_flights: 13, completed_flights: 11, delayed_flights: 2, on_time_percentage: 85 },
              { date: '2025-02-27', total_flights: 15, completed_flights: 12, delayed_flights: 3, on_time_percentage: 80 },
              { date: '2025-02-28', total_flights: 17, completed_flights: 15, delayed_flights: 2, on_time_percentage: 88 },
              { date: '2025-03-01', total_flights: 15, completed_flights: 12, delayed_flights: 3, on_time_percentage: 80 }
            ]
          };
          
          setReport(mockReport);
        }
        
        setError(null);
      } catch (error) {
        console.error('Error fetching report data:', error);
        setError(t('reports.errorLoadingReport'));
      } finally {
        setLoading(false);
      }
    };

    fetchReportData();
  }, [reportType, dateRange, t]);

  const handleExportReport = async (format: 'json' | 'csv') => {
    try {
      setLoading(true);
      
      let endpoint = `http://localhost:8000/api/reports/export/${format}`;
      let params: any = { report_type: 'daily' };
      
      if (reportType === 'daily') {
        params.report_type = 'daily';
        
        if (dateRange === 'today') {
          const today = new Date().toISOString().split('T')[0];
          params.date = today;
        } else if (dateRange === 'yesterday') {
          const yesterday = new Date();
          yesterday.setDate(yesterday.getDate() - 1);
          params.date = yesterday.toISOString().split('T')[0];
        }
      } else {
        params.report_type = 'weekly';
        
        if (dateRange === 'week') {
          // Use default (last 7 days)
        } else if (dateRange === 'month') {
          const endDate = new Date();
          params.end_date = endDate.toISOString().split('T')[0];
        }
      }
      
      const response = await axios.get(endpoint, { params });
      
      // In a real app, this would trigger a file download
      console.log(`Report exported: ${response.data.filename}`);
      alert(t('reports.exportSuccess'));
      
    } catch (error) {
      console.error(`Error exporting report to ${format}:`, error);
      setError(t('reports.exportError'));
    } finally {
      setLoading(false);
    }
  };

  const getReportTypeTitle = () => {
    switch (reportType) {
      case 'daily':
        return t('reports.dailySummary');
      case 'performance':
        return t('reports.performanceMetrics');
      case 'competitor':
        return t('reports.competitorAnalysis');
      case 'operational':
        return t('reports.operationalEfficiency');
      default:
        return t('reports.title');
    }
  };

  const getDateRangeText = () => {
    switch (dateRange) {
      case 'today':
        return t('reports.today');
      case 'yesterday':
        return t('reports.yesterday');
      case 'week':
        return t('reports.lastWeek');
      case 'month':
        return t('reports.lastMonth');
      case 'custom':
        return t('reports.customRange');
      default:
        return '';
    }
  };

  // Prepare data for flight status pie chart
  const prepareFlightStatusData = () => {
    if (!report) return [];
    
    return [
      { name: t('schedule.onTime'), value: report.completed_flights - report.delayed_flights },
      { name: t('schedule.delayed'), value: report.delayed_flights },
      { name: t('schedule.cancelled'), value: report.total_flights - report.completed_flights }
    ];
  };

  // Prepare data for competitor comparison
  const prepareCompetitorData = () => {
    if (!report || !report.competitor_stats) return [];
    
    const ourData = {
      name: t('reports.competitorComparison'),
      total: report.total_flights,
      completed: report.completed_flights,
      onTime: report.completed_flights - report.delayed_flights
    };
    
    const competitorData = Object.entries(report.competitor_stats).map(([name, stats]: [string, any]) => ({
      name,
      total: stats.total,
      completed: stats.completed,
      onTime: stats.completed - (stats.total * 0.1) // Assuming 10% delay rate if not provided
    }));
    
    return [ourData, ...competitorData];
  };

  return (
    <div className="report-container">
      <div className="report-header">
        <div>
          <h3>{getReportTypeTitle()}</h3>
          <p className="date-range">{t('reports.timePeriod')}: {getDateRangeText()}</p>
        </div>
        <div className="action-buttons">
          <button 
            className="btn-download" 
            onClick={() => handleExportReport('json')}
            disabled={loading || !report}
          >
            {t('reports.exportJSON')}
          </button>
          <button 
            className="btn-download" 
            onClick={() => handleExportReport('csv')}
            disabled={loading || !report}
          >
            {t('reports.exportCSV')}
          </button>
        </div>
      </div>
      
      {loading && <div className="loading-indicator">{t('reports.loadingReport')}</div>}
      {error && <div className="error-message">{error}</div>}
      
      {!loading && !error && !report && (
        <div className="no-data-message">{t('reports.noReportData')}</div>
      )}
      
      {!loading && !error && report && (
        <div>
          <div className="stat-card">
            <h4>{t('reports.totalFlights')}</h4>
            <div className="stat-value">{report.total_flights}</div>
          </div>
          
          <div className="stat-card">
            <h4>{t('reports.completedFlights')}</h4>
            <div className="stat-value">{report.completed_flights}</div>
          </div>
          
          <div className="stat-card">
            <h4>{t('reports.delayedFlights')}</h4>
            <div className="stat-value">{report.delayed_flights}</div>
          </div>
          
          <div className="stat-card">
            <h4>{t('reports.onTimePercentage')}</h4>
            <div className="stat-value">{report.on_time_percentage}%</div>
          </div>
          
          <div className="stat-card">
            <h4>{t('reports.averageDelay')}</h4>
            <div className="stat-value">{report.average_delay_minutes} min</div>
          </div>
          
          {report.total_alerts !== undefined && (
            <div className="stat-card">
              <h4>{t('reports.totalAlerts')}</h4>
              <div className="stat-value">{report.total_alerts}</div>
            </div>
          )}
          
          <div className="chart-container">
            <h4>{t('reports.flightStatusDistribution')}</h4>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={prepareFlightStatusData()}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                >
                  {prepareFlightStatusData().map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
          
          {report.competitor_stats && (
            <div className="chart-container">
              <h4>{t('reports.competitorComparison')}</h4>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart
                  data={prepareCompetitorData()}
                  margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="total" name={t('reports.totalFlights')} fill="#8884d8" />
                  <Bar dataKey="completed" name={t('reports.completedFlights')} fill="#82ca9d" />
                  <Bar dataKey="onTime" name={t('schedule.onTime')} fill="#ffc658" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
          
          {report.daily_reports && (
            <div className="chart-container">
              <h4>{t('reports.dailyFlightActivity')}</h4>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart
                  data={report.daily_reports}
                  margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="total_flights" name={t('reports.totalFlights')} stroke="#8884d8" />
                  <Line type="monotone" dataKey="completed_flights" name={t('reports.completedFlights')} stroke="#82ca9d" />
                  <Line type="monotone" dataKey="on_time_percentage" name={t('reports.onTimePercentage')} stroke="#ffc658" yAxisId={1} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Report;
