import React, { useEffect } from 'react';
import { useCoAgent } from '../contexts/CoAgentContext';
import ResearchCanvas from './ResearchCanvas';

const Main: React.FC = () => {
  const { state, dispatch } = useCoAgent();

  useEffect(() => {
    if (process.env.NODE_ENV === 'development') {
      console.log('Main state updated:', {
        hasReport: !!state.report,
        reportLength: state.report?.length,
        stateKeys: Object.keys(state)
      });
    }
  }, [state]);

  return (
    <div className="flex flex-col h-screen">
      <ResearchCanvas />
      {process.env.NODE_ENV === 'development' && (
        <div className="fixed bottom-0 right-0 p-2 bg-gray-100 text-xs">
          <pre>
            {JSON.stringify({
              hasReport: !!state.report,
              reportLength: state.report?.length,
            }, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default Main; 