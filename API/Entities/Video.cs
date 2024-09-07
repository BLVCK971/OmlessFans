namespace Omless.Api.Entities;

public class Video
{
	public int Id { get; set; }
	public string Title { get; set; } = string.Empty;
	public string Description { get; set; } = string.Empty;
	public DateTime CreatedAt { get; set; }
	public DateTime UpdatedAt { get; set; } = DateTime.Now;

	public string Url { get; set; } = string.Empty;
	//public string ThumbnailUrl { get; set; } = string.Empty;
	//public int Views { get; set; }
	//public int Likes { get; set; }
	
	public Guid OmlessId { get; set; }
	public Omless Omless { get; set; }
}
