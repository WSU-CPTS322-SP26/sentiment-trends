const TopicDetailPageSkeleton = () => {
  return (
    <div
      className="space-y-3"
      aria-busy="true"
      aria-label="Loading topic details"
    >
      <div className="rounded-2xl border-2 border-neutral-200 bg-score-tint px-4 py-3 shadow-sm">
        <div className="h-4 w-28 rounded-md bg-neutral-200 animate-pulse" />
        <div className="mt-2 h-9 w-56 max-w-full rounded-lg bg-neutral-200 animate-pulse" />
        <div className="mt-2 h-3 w-full max-w-lg rounded-md bg-neutral-200 animate-pulse" />
      </div>

      <div className="rounded-xl border border-gray-200 bg-gray-50 p-4">
        <div className="mb-3 flex items-center gap-2">
          <div className="size-4 shrink-0 rounded bg-neutral-200 animate-pulse" />
          <div className="h-4 w-52 max-w-full rounded-md bg-neutral-200 animate-pulse" />
        </div>
        <div className="h-6 w-full rounded-md bg-neutral-200 animate-pulse" />
      </div>

      <div className="space-y-3 rounded-2xl border-2 border-neutral-200 bg-white px-6 py-5 shadow-sm">
        <div className="h-6 w-36 rounded-md bg-neutral-200 animate-pulse" />
        <div className="space-y-2">
          <div className="h-3 w-full rounded-md bg-neutral-200 animate-pulse" />
          <div className="h-3 w-full rounded-md bg-neutral-200 animate-pulse" />
          <div className="h-3 max-w-[90%] rounded-md bg-neutral-200 animate-pulse" />
        </div>
        <div className="h-9 w-44 rounded-lg bg-neutral-200 animate-pulse" />
      </div>

      <div className="space-y-4">
        <div className="h-5 w-36 rounded-md bg-neutral-200 animate-pulse" />
        {[0, 1].map((i) => (
          <div
            key={i}
            className="space-y-3 rounded-xl border border-neutral-200 bg-white p-4 shadow-sm"
          >
            <div className="h-6 w-48 max-w-full rounded-md bg-neutral-200 animate-pulse" />
            <div className="h-4 w-24 rounded-md bg-neutral-200 animate-pulse" />
            <div className="space-y-2">
              <div className="h-3 w-full rounded-md bg-neutral-200 animate-pulse" />
              <div className="h-3 w-full rounded-md bg-neutral-200 animate-pulse" />
              <div className="h-3 max-w-[90%] rounded-md bg-neutral-200 animate-pulse" />
            </div>
            <div className="h-3 w-32 rounded-md bg-neutral-200 animate-pulse" />
          </div>
        ))}
      </div>
    </div>
  );
};

export default TopicDetailPageSkeleton;
