function AppLayout({ children }: any) {
  return (
    <div className="bg-primary w-screen h-screen p-6 flex flex-col">
      {children}
    </div>
  );
}

export default AppLayout;
