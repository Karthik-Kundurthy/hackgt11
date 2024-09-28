function AppLayout({ children }: any) {
  return (
    <div className="bg-primary w-screen h-screen p-6">
      <main>{children}</main>
    </div>
  );
}

export default AppLayout;
