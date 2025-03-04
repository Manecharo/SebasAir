import React, { useState } from 'react';
import Report from './Report';
import useTranslation from '../i18n/useTranslation';

const Reports: React.FC = () => {
  const { t } = useTranslation();
  const [dateRange, setDateRange] = useState<string>('week');
  const [reportType, setReportType] = useState<string>('daily');
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [showReport, setShowReport] = useState<boolean>(false);

  const handleDateRangeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setDateRange(e.target.value);
    setShowReport(false);
  };

  const handleReportTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setReportType(e.target.value);
    setShowReport(false);
  };

  const handleGenerateReport = () => {
    setIsGenerating(true);
    
    // Simulate API call delay
    setTimeout(() => {
      setIsGenerating(false);
      setShowReport(true);
    }, 1000);
  };

  return (
    <div className="reports-container">
      <div className="schedule-header">
        <h2 className="schedule-title">{t('reports.title')}</h2>
        <p className="subtitle">{t('reports.subtitle')}</p>
      </div>
      
      <div className="report-filters">
        <div className="filter-group">
          <label htmlFor="date-range">{t('reports.dateRange')}:</label>
          <select 
            id="date-range" 
            value={dateRange} 
            onChange={handleDateRangeChange}
            disabled={isGenerating}
          >
            <option value="today">{t('reports.today')}</option>
            <option value="yesterday">{t('reports.yesterday')}</option>
            <option value="week">{t('reports.lastWeek')}</option>
            <option value="month">{t('reports.lastMonth')}</option>
            <option value="custom">{t('reports.customRange')}</option>
          </select>
        </div>
        
        <div className="filter-group">
          <label htmlFor="report-type">{t('reports.reportType')}:</label>
          <select 
            id="report-type" 
            value={reportType} 
            onChange={handleReportTypeChange}
            disabled={isGenerating}
          >
            <option value="daily">{t('reports.dailySummary')}</option>
            <option value="performance">{t('reports.performanceMetrics')}</option>
            <option value="competitor">{t('reports.competitorAnalysis')}</option>
            <option value="operational">{t('reports.operationalEfficiency')}</option>
          </select>
        </div>
        
        <button 
          className={`btn-generate ${isGenerating ? 'loading' : ''}`}
          onClick={handleGenerateReport}
          disabled={isGenerating}
        >
          {isGenerating ? t('common.loading') : t('reports.generateReport')}
        </button>
      </div>
      
      {showReport && <Report reportType={reportType} dateRange={dateRange} />}
    </div>
  );
};

export default Reports;
