const TopicDetailSkeleton = () => (
  <div className="space-y-4" aria-busy="true">
    <div className="h-24 rounded-2xl border-2 border-neutral-200 bg-neutral-100 animate-pulse" />
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className="h-24 rounded-2xl border-2 border-neutral-200 bg-neutral-100 animate-pulse"
        />
      ))}
    </div>
    <div className="h-32 rounded-xl border border-neutral-200 bg-neutral-100 animate-pulse" />
    <div className="space-y-3">
      {[1, 2].map((i) => (
        <div
          key={i}
          className="h-28 rounded-xl border border-neutral-200 bg-neutral-100 animate-pulse"
        />
      ))}
    </div>
  </div>
);

export default TopicDetailSkeleton;
