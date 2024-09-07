var builder = WebApplication.CreateBuilder(args);

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddDbContext<ApplicationDbContext>(options =>
		options.LogTo(Console.WriteLine),(_, level) => level == LogLevel.Information);

var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.Run();
