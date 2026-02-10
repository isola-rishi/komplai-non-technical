/**
 * Komplai Design System - React Component Examples
 * This file demonstrates how to use the Komplai design system in React artifacts
 */

import React from 'react';

// Example 1: Hero Section with Call-to-Action
export const HeroSection = () => {
  return (
    <div style={{
      background: 'rgb(2, 31, 14)',
      padding: '96px 24px',
      textAlign: 'center',
      color: 'rgb(255, 255, 255)'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '8px',
          marginBottom: '24px'
        }}>
          <div style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            background: 'rgb(69, 209, 99)'
          }} />
          <span style={{ fontSize: '14px', fontWeight: '500' }}>
            Welcome to Komplai
          </span>
        </div>

        <h1 style={{
          fontFamily: '"Playfair Display", serif',
          fontSize: '72px',
          fontWeight: '700',
          lineHeight: '1.1',
          letterSpacing: '-0.02em',
          marginBottom: '24px'
        }}>
          Audit-ready finance automation for your business.
        </h1>

        <p style={{
          fontSize: '18px',
          lineHeight: '1.6',
          maxWidth: '900px',
          margin: '0 auto 32px',
          opacity: '0.9'
        }}>
          Komplai handles the tedious 90% of bookkeeping, reconciliation, and reporting
          through its finance agent - Larry. Close your books 65% faster, eliminate manual
          errors, and reclaim your team's time for high-level strategy.
        </p>

        <button style={{
          background: 'rgb(22, 84, 46)',
          color: 'rgb(255, 255, 255)',
          padding: '12px 24px',
          borderRadius: '8px',
          border: 'none',
          fontSize: '16px',
          fontWeight: '500',
          cursor: 'pointer',
          transition: 'background 0.2s ease'
        }}>
          Get Started Now →
        </button>
      </div>
    </div>
  );
};

// Example 2: Status Dashboard Card
export const StatusCard = ({ title, items }) => {
  return (
    <div style={{
      background: 'rgb(58, 99, 81)',
      borderRadius: '16px',
      padding: '32px',
      color: 'rgb(255, 255, 255)'
    }}>
      <h3 style={{
        fontFamily: '"Playfair Display", serif',
        fontSize: '28px',
        marginBottom: '24px'
      }}>
        {title}
      </h3>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {items.map((item, index) => (
          <TaskItem key={index} {...item} />
        ))}
      </div>
    </div>
  );
};

// Example 3: Task Item Component
const TaskItem = ({ title, status, progress, assignee }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'rgb(69, 209, 99)';
      case 'pending': return 'rgb(255, 238, 189)';
      default: return 'rgb(102, 102, 102)';
    }
  };

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '16px 24px',
      background: 'rgba(255, 255, 255, 0.1)',
      borderRadius: '10px',
      transition: 'background 0.2s ease'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{
          width: '24px',
          height: '24px',
          borderRadius: '50%',
          background: getStatusColor(status),
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}>
          {status === 'completed' && '✓'}
        </div>
        <span style={{ fontWeight: '500' }}>{title}</span>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{
          width: '40px',
          height: '40px',
          borderRadius: '50%',
          background: 'rgb(34, 34, 34)',
          color: 'rgb(255, 255, 255)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '14px',
          fontWeight: '600',
          border: '2px solid rgba(255, 255, 255, 0.2)'
        }}>
          {assignee}
        </div>
        <span style={{ fontSize: '14px' }}>{progress}</span>
      </div>
    </div>
  );
};

// Example 4: Alert Cards
export const AlertCard = ({ type, title, message }) => {
  const alertStyles = {
    risk: {
      background: 'rgba(255, 100, 100, 0.1)',
      border: '1px solid rgba(255, 100, 100, 0.3)',
      color: 'rgb(255, 100, 100)'
    },
    growth: {
      background: 'rgba(69, 209, 99, 0.1)',
      border: '1px solid rgba(69, 209, 99, 0.3)',
      color: 'rgb(69, 209, 99)'
    },
    observation: {
      background: 'rgba(255, 255, 255, 0.05)',
      border: '1px solid rgba(255, 255, 255, 0.2)',
      color: 'rgb(255, 255, 255)'
    }
  };

  const style = alertStyles[type] || alertStyles.observation;

  return (
    <div style={{
      ...style,
      padding: '16px',
      borderRadius: '10px',
      marginBottom: '16px'
    }}>
      <div style={{
        fontWeight: '700',
        textTransform: 'uppercase',
        letterSpacing: '0.5px',
        fontSize: '12px',
        marginBottom: '8px'
      }}>
        {title}
      </div>
      <div style={{ fontSize: '14px' }}>
        {message}
      </div>
    </div>
  );
};

// Example 5: Progress Bar Component
export const ProgressBar = ({ value, total, variant = 'complete' }) => {
  const percentage = (value / total) * 100;

  const variantColors = {
    complete: 'rgb(69, 209, 99)',
    partial: 'rgb(255, 165, 0)',
    inactive: 'rgb(102, 102, 102)'
  };

  return (
    <div style={{
      width: '100%',
      height: '8px',
      background: 'rgb(235, 235, 235)',
      borderRadius: '40px',
      overflow: 'hidden'
    }}>
      <div style={{
        width: `${percentage}%`,
        height: '100%',
        background: variantColors[variant],
        borderRadius: '40px',
        transition: 'width 0.3s ease'
      }} />
    </div>
  );
};

// Example 6: Feature Card (Light Background)
export const FeatureCard = ({ title, description, icon }) => {
  return (
    <div style={{
      background: 'rgb(255, 255, 255)',
      border: '1px solid rgb(235, 235, 235)',
      borderRadius: '16px',
      padding: '32px',
      transition: 'transform 0.2s ease'
    }}>
      <div style={{
        fontSize: '32px',
        marginBottom: '16px'
      }}>
        {icon}
      </div>

      <h3 style={{
        fontFamily: '"Playfair Display", serif',
        fontSize: '24px',
        color: 'rgb(34, 34, 34)',
        marginBottom: '12px'
      }}>
        {title}
      </h3>

      <p style={{
        color: 'rgb(102, 102, 102)',
        lineHeight: '1.6',
        fontSize: '15px'
      }}>
        {description}
      </p>
    </div>
  );
};

// Example 7: Complete Dashboard Layout
export default function KomplaiDashboard() {
  const tasks = [
    { title: 'Invoice Validation', status: 'completed', progress: '25/25 Done', assignee: 'RA' },
    { title: 'Reviewing Reconciled Transactions', status: 'pending', progress: '35/50 Tasks', assignee: 'AV' },
    { title: 'Resolve Unreconciled Transactions', status: 'pending', progress: '10/20 Tasks', assignee: 'RA' }
  ];

  return (
    <div style={{ background: 'rgb(2, 31, 14)', minHeight: '100vh', padding: '48px 24px' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <HeroSection />

        <div style={{ marginTop: '48px' }}>
          <StatusCard title="Current Close Status" items={tasks} />
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '16px',
          marginTop: '24px'
        }}>
          <AlertCard
            type="risk"
            title="RISK ALERT"
            message="Two unresolved enterprise receivables could delay close by up to 48 hours if not cleared this week."
          />
          <AlertCard
            type="growth"
            title="GROWTH"
            message="Close execution is 38% ahead of last month, driven by automated validation and reconciliations."
          />
          <AlertCard
            type="observation"
            title="OBSERVATION"
            message="Accruals are the only remaining critical path item. Starting now keeps Day-30 pressure off the team."
          />
        </div>
      </div>
    </div>
  );
}
