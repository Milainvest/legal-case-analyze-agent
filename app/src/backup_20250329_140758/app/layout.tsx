import { ResearchStateProvider } from '@/lib/research-state-provider';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ModelSelectorProvider>
          <ResearchStateProvider>
            {children}
          </ResearchStateProvider>
        </ModelSelectorProvider>
      </body>
    </html>
  );
} 