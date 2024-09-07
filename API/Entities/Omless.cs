namespace Omless.Api.Entities;

public class User : BaseEntity
{
	public Guid Id { get; set; }
	public string Name { get; set; } = string.Empty;
	public IEnumerable<Video> Videos { get; set; } = new List<Video>();
	public IEnumerable<Fan> Fans { get; set; } = new List<Fan>();
	public IEnumerable<Don> Dons { get; set; } = new List<Don>();
}
